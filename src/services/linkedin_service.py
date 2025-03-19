"""
LinkedIn service for the SearchAgent application.
Handles interaction with the LinkedIn API.
"""
import json
import requests
from typing import Dict, Any, Optional
import logging
from SearchAgent.src.config import config

# Set up logging
logger = logging.getLogger(__name__)


class LinkedinService:
    """
    Service for interacting with the LinkedIn API.
    Follows the Service design pattern.
    """
    
    def __init__(self):
        """Initialize the LinkedIn service."""
        self.api_key = config.get("SCRAPIN_API_KEY", "")
        if not self.api_key:
            logger.warning("SCRAPIN_API_KEY not found in configuration.")
    
    def scrape_linkedin_profile(self, linkedin_profile_url: str) -> Dict[str, Any]:
        """
        Scrape a LinkedIn profile.
        
        Args:
            linkedin_profile_url: The URL of the LinkedIn profile
            
        Returns:
            Dictionary containing the LinkedIn profile data
            
        Raises:
            ValueError: If the API key is not configured
            requests.RequestException: If there is an error with the API request
        """
        if not self.api_key:
            raise ValueError("SCRAPIN_API_KEY not configured. Cannot scrape LinkedIn profile.")
        
        api_endpoint = "https://api.scrapin.be/v1/extract/person"
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
        }
        data = {"url": linkedin_profile_url}
        
        try:
            response = requests.post(api_endpoint, json=data, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error scraping LinkedIn profile: {str(e)}")
            # Return a minimal representation to ensure the application can continue
            return {"error": str(e), "profile_pic": "", "summary": "", "experiences": []}
    
    def get_mock_profile(self, linkedin_profile_url: str) -> Dict[str, Any]:
        """
        Get a mock LinkedIn profile for testing purposes.
        
        Args:
            linkedin_profile_url: The URL of the LinkedIn profile (unused in mock)
            
        Returns:
            Dictionary containing mock LinkedIn profile data
        """
        return {
            "name": "John Doe",
            "summary": "Experienced software engineer with a passion for AI and machine learning.",
            "photoUrl": "https://example.com/profile.jpg",
            "experiences": [
                {
                    "title": "Senior Software Engineer",
                    "company": "Tech Corp",
                    "date_range": "2020 - Present"
                },
                {
                    "title": "Software Engineer",
                    "company": "Startup Inc",
                    "date_range": "2018 - 2020"
                }
            ],
            "educations": [
                {
                    "degree": "Master's Degree in Computer Science",
                    "school": "Tech University",
                    "date_range": "2016 - 2018"
                }
            ]
        } 