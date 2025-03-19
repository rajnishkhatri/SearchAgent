"""
Twitter service for the SearchAgent application.
Handles interaction with the Twitter API.
"""
import json
import logging
from typing import List, Dict, Any, Optional
import tweepy
from SearchAgent.src.config import config

# Set up logging
logger = logging.getLogger(__name__)


class TwitterService:
    """
    Service for interacting with the Twitter API.
    Follows the Service design pattern.
    """
    
    def __init__(self):
        """Initialize the Twitter service."""
        self.api_key = config.get("TWITTER_API_KEY", "")
        self.api_secret = config.get("TWITTER_API_SECRET", "")
        self.access_token = config.get("TWITTER_ACCESS_TOKEN", "")
        self.access_secret = config.get("TWITTER_ACCESS_SECRET", "")
        self.client = self._initialize_client()
    
    def _initialize_client(self) -> Optional[tweepy.Client]:
        """
        Initialize the Twitter client.
        
        Returns:
            tweepy.Client if API keys are configured, None otherwise
        """
        if not all([self.api_key, self.api_secret, self.access_token, self.access_secret]):
            logger.warning("Twitter API credentials not fully configured.")
            return None
        
        try:
            return tweepy.Client(
                consumer_key=self.api_key,
                consumer_secret=self.api_secret,
                access_token=self.access_token,
                access_token_secret=self.access_secret
            )
        except Exception as e:
            logger.error(f"Error initializing Twitter client: {str(e)}")
            return None
    
    def scrape_user_tweets(self, username: str, max_tweets: int = 5) -> List[str]:
        """
        Scrape tweets from a Twitter user.
        
        Args:
            username: The Twitter username
            max_tweets: Maximum number of tweets to retrieve (default: 5)
            
        Returns:
            List of tweets as strings
            
        Raises:
            ValueError: If the Twitter client is not initialized
            tweepy.TweepyException: If there is an error with the Twitter API request
        """
        if not self.client:
            raise ValueError("Twitter client not initialized. Cannot scrape tweets.")
        
        try:
            # First, get the user ID
            user = self.client.get_user(username=username)
            if not user or not user.data:
                logger.warning(f"User {username} not found on Twitter.")
                return []
            
            user_id = user.data.id
            
            # Then get the tweets
            tweets = self.client.get_users_tweets(
                id=user_id, 
                max_results=max_tweets,
                exclude="retweets,replies"
            )
            
            if not tweets or not tweets.data:
                logger.info(f"No tweets found for user {username}.")
                return []
            
            return [tweet.text for tweet in tweets.data]
        except tweepy.TweepyException as e:
            logger.error(f"Error scraping Twitter for user {username}: {str(e)}")
            return []
    
    def scrape_user_tweets_mock(self, username: str, max_tweets: int = 5) -> List[str]:
        """
        Get mock tweets for testing purposes.
        
        Args:
            username: The Twitter username (unused in mock)
            max_tweets: Maximum number of tweets to retrieve (default: 5)
            
        Returns:
            List of mock tweets as strings
        """
        return [
            "Excited about the latest developments in AI! #MachineLearning #Innovation",
            "Just published a new article on deep learning techniques. Check it out!",
            "Working on a new project using transformer models. Stay tuned for updates.",
            "Had a great meeting with the team today discussing our AI roadmap for 2023.",
            "Reading 'Artificial Intelligence: A Modern Approach' for the third time. Still learning new things!"
        ][:max_tweets] 