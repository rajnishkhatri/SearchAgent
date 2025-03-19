"""
Profile chains for the SearchAgent application.
Contains the chains for generating summaries, interests, and ice breakers.
"""
import logging
from typing import List, Dict, Any, Optional
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from SearchAgent.src.models.output_models import Summary, IceBreaker, TopicOfInterest
from SearchAgent.src.utils.output_parsers import (
    summary_parser, 
    ice_breaker_parser, 
    topics_of_interest_parser
)
from SearchAgent.src.config import config

# Set up logging
logger = logging.getLogger(__name__)


class ProfileChainFactory:
    """
    Factory for creating profile chains.
    Follows the Factory design pattern.
    """
    
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        """
        Initialize the profile chain factory.
        
        Args:
            model_name: The name of the OpenAI model to use
        """
        self.openai_api_key = config.get("OPENAI_API_KEY", "")
        self.llm = self._initialize_llm(model_name)
    
    def _initialize_llm(self, model_name: str) -> ChatOpenAI:
        """
        Initialize the language model.
        
        Args:
            model_name: The name of the OpenAI model to use
            
        Returns:
            ChatOpenAI model
            
        Raises:
            ValueError: If the OpenAI API key is not configured
        """
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY not configured. Cannot initialize profile chains.")
        
        return ChatOpenAI(
            temperature=0.2,
            model=model_name,
            api_key=self.openai_api_key
        )
    
    def _format_tweets(self, tweets: List[str]) -> str:
        """
        Format tweets into a string.
        
        Args:
            tweets: List of tweets
            
        Returns:
            String representation of tweets
        """
        return " ".join(tweets)
    
    def create_summary_chain(self) -> RunnablePassthrough:
        """
        Create a chain for generating summaries.
        
        Returns:
            Chain for generating summaries
        """
        prompt = ChatPromptTemplate.from_template(
            """
            I want you to extract the following information from the provided text and twitter posts:
            1. A summary of the person's background, experience, and skills
            2. Interesting facts about the person
            
            Here is the information from their profile:
            {information}
            
            Here are their recent twitter posts:
            {twitter_posts}
            
            {format_instructions}
            """
        )
        
        return (
            {
                "information": lambda x: x["information"],
                "twitter_posts": lambda x: self._format_tweets(x["twitter_posts"]),
                "format_instructions": summary_parser.get_format_instructions(),
            }
            | prompt
            | self.llm
            | summary_parser
        )
    
    def create_interests_chain(self) -> RunnablePassthrough:
        """
        Create a chain for generating interests.
        
        Returns:
            Chain for generating interests
        """
        prompt = ChatPromptTemplate.from_template(
            """
            I want you to extract a list of topics that might interest the person based on the provided text and twitter posts.
            
            Here is the information from their profile:
            {information}
            
            Here are their recent twitter posts:
            {twitter_posts}
            
            {format_instructions}
            """
        )
        
        return (
            {
                "information": lambda x: x["information"],
                "twitter_posts": lambda x: self._format_tweets(x["twitter_posts"]),
                "format_instructions": topics_of_interest_parser.get_format_instructions(),
            }
            | prompt
            | self.llm
            | topics_of_interest_parser
        )
    
    def create_ice_breaker_chain(self) -> RunnablePassthrough:
        """
        Create a chain for generating ice breakers.
        
        Returns:
            Chain for generating ice breakers
        """
        prompt = ChatPromptTemplate.from_template(
            """
            I want you to generate 5 ice breakers that I can use when I meet with this person.
            
            Here is the information from their profile:
            {information}
            
            Here are their recent twitter posts:
            {twitter_posts}
            
            {format_instructions}
            """
        )
        
        return (
            {
                "information": lambda x: x["information"],
                "twitter_posts": lambda x: self._format_tweets(x["twitter_posts"]),
                "format_instructions": ice_breaker_parser.get_format_instructions(),
            }
            | prompt
            | self.llm
            | ice_breaker_parser
        ) 