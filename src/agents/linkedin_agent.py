"""
LinkedIn agent for the SearchAgent application.
Uses LangChain to find LinkedIn profiles for a person.
"""
import logging
from typing import Optional
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from SearchAgent.src.config import config

# Set up logging
logger = logging.getLogger(__name__)


class LinkedinAgent:
    """
    Agent for looking up LinkedIn profiles.
    Uses the Chain of Responsibility and Strategy patterns.
    """
    
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        """
        Initialize the LinkedIn agent.
        
        Args:
            model_name: The name of the OpenAI model to use
        """
        self.openai_api_key = config.get("OPENAI_API_KEY", "")
        self.llm = self._initialize_llm(model_name)
        self.prompt = self._create_prompt()
    
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
            raise ValueError("OPENAI_API_KEY not configured. Cannot initialize LinkedIn agent.")
        
        return ChatOpenAI(
            temperature=0.0,
            model=model_name,
            api_key=self.openai_api_key
        )
    
    def _create_prompt(self) -> ChatPromptTemplate:
        """
        Create the prompt for the LinkedIn agent.
        
        Returns:
            ChatPromptTemplate for the LinkedIn agent
        """
        template = """
        I want you to find the LinkedIn URL for {name}.
        
        Your response should be the LinkedIn URL only, nothing else.
        If you can't find the LinkedIn URL, respond with "No LinkedIn profile found".
        """
        
        return ChatPromptTemplate.from_template(template)
    
    def lookup(self, name: str) -> str:
        """
        Look up a LinkedIn profile for a person.
        
        Args:
            name: The name of the person to look up
            
        Returns:
            LinkedIn profile URL or error message
            
        Raises:
            Exception: If there is an error with the language model
        """
        try:
            logger.info(f"Looking up LinkedIn profile for {name}")
            
            # Create the chain
            chain = self.prompt | self.llm
            
            # Run the chain
            linkedin_username = chain.invoke({"name": name})
            
            # Clean up the response
            linkedin_username = linkedin_username.content.strip()
            
            logger.info(f"Found LinkedIn profile: {linkedin_username}")
            return linkedin_username
        except Exception as e:
            logger.error(f"Error looking up LinkedIn profile for {name}: {str(e)}")
            return "No LinkedIn profile found" 