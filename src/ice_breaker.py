"""
Ice Breaker service for the SearchAgent application.
Core logic for generating ice breakers.
"""
import logging
from typing import Tuple
from SearchAgent.src.agents.linkedin_agent import LinkedinAgent
from SearchAgent.src.agents.twitter_agent import TwitterAgent
from SearchAgent.src.services.linkedin_service import LinkedinService
from SearchAgent.src.services.twitter_service import TwitterService
from SearchAgent.src.chains.profile_chains import ProfileChainFactory
from SearchAgent.src.models.output_models import Summary, TopicOfInterest, IceBreaker

# Set up logging
logger = logging.getLogger(__name__)


class IceBreakerService:
    """
    Service for generating ice breakers.
    Follows the Facade design pattern to hide the complexity of the subsystems.
    """
    
    def __init__(self, use_mock: bool = False):
        """
        Initialize the Ice Breaker service.
        
        Args:
            use_mock: Whether to use mock data instead of real API calls
        """
        self.linkedin_agent = LinkedinAgent()
        self.twitter_agent = TwitterAgent()
        self.linkedin_service = LinkedinService()
        self.twitter_service = TwitterService()
        self.profile_chain_factory = ProfileChainFactory()
        self.use_mock = use_mock
    
    def ice_break_with(self, name: str) -> Tuple[Summary, TopicOfInterest, IceBreaker, str]:
        """
        Generate ice breakers for a person.
        
        Args:
            name: The name of the person
            
        Returns:
            Tuple of (Summary, TopicOfInterest, IceBreaker, profile_pic_url)
            
        Raises:
            Exception: If there is an error generating ice breakers
        """
        try:
            # Look up LinkedIn profile
            linkedin_username = self.linkedin_agent.lookup(name=name)
            
            # Scrape LinkedIn profile
            if self.use_mock:
                linkedin_data = self.linkedin_service.get_mock_profile(linkedin_username)
            else:
                linkedin_data = self.linkedin_service.scrape_linkedin_profile(linkedin_username)
            
            # Look up Twitter profile
            twitter_username = self.twitter_agent.lookup(name=name)
            
            # Scrape Twitter profile
            if self.use_mock or not self.twitter_service.client:
                tweets = self.twitter_service.scrape_user_tweets_mock(twitter_username)
            else:
                tweets = self.twitter_service.scrape_user_tweets(twitter_username)
            
            # Get summary chain
            summary_chain = self.profile_chain_factory.create_summary_chain()
            summary_and_facts: Summary = summary_chain.invoke(
                input={"information": linkedin_data, "twitter_posts": tweets},
            )
            
            # Get interests chain
            interests_chain = self.profile_chain_factory.create_interests_chain()
            interests: TopicOfInterest = interests_chain.invoke(
                input={"information": linkedin_data, "twitter_posts": tweets}
            )
            
            # Get ice breaker chain
            ice_breaker_chain = self.profile_chain_factory.create_ice_breaker_chain()
            ice_breakers: IceBreaker = ice_breaker_chain.invoke(
                input={"information": linkedin_data, "twitter_posts": tweets}
            )
            
            # Get profile picture URL
            profile_pic_url = linkedin_data.get("photoUrl", "")
            
            logger.info(f"Generated ice breakers for {name}")
            return (
                summary_and_facts,
                interests,
                ice_breakers,
                profile_pic_url,
            )
        except Exception as e:
            logger.error(f"Error generating ice breakers for {name}: {str(e)}")
            raise 