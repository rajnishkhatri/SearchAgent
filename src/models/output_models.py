"""
Models for the output of the SearchAgent application.
Uses Pydantic for data validation and serialization.
"""
from typing import List, Dict, Any
from pydantic import BaseModel, Field


class Summary(BaseModel):
    """Model representing a summary of a person's profile."""
    summary: str = Field(description="Summary of the person's professional background")
    facts: List[str] = Field(description="Interesting facts about the person")

    def to_dict(self) -> Dict[str, Any]:
        """Convert the model to a dictionary."""
        return {"summary": self.summary, "facts": self.facts}


class IceBreaker(BaseModel):
    """Model representing ice breakers for a conversation."""
    ice_breakers: List[str] = Field(description="List of ice breakers to start a conversation")

    def to_dict(self) -> Dict[str, Any]:
        """Convert the model to a dictionary."""
        return {"ice_breakers": self.ice_breakers}


class TopicOfInterest(BaseModel):
    """Model representing topics of interest for a person."""
    topics_of_interest: List[str] = Field(
        description="Topics that might interest the person"
    )

    def to_dict(self) -> Dict[str, Any]:
        """Convert the model to a dictionary."""
        return {"topics_of_interest": self.topics_of_interest}


class ProfileInfo(BaseModel):
    """Model representing aggregated profile information."""
    summary: Summary
    interests: TopicOfInterest
    ice_breakers: IceBreaker
    profile_pic_url: str = Field(description="URL to the person's profile picture")

    def to_dict(self) -> Dict[str, Any]:
        """Convert the model to a dictionary."""
        return {
            "summary_and_facts": self.summary.to_dict(),
            "interests": self.interests.to_dict(),
            "ice_breakers": self.ice_breakers.to_dict(),
            "picture_url": self.profile_pic_url,
        } 