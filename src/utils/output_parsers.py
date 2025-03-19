"""
Output parsers for LangChain models.
"""
from langchain_core.output_parsers import PydanticOutputParser
from SearchAgent.src.models.output_models import Summary, IceBreaker, TopicOfInterest


class OutputParserFactory:
    """
    Factory class for creating output parsers.
    Follows the Factory design pattern.
    """
    
    @staticmethod
    def create_summary_parser() -> PydanticOutputParser:
        """Create a parser for Summary objects."""
        return PydanticOutputParser(pydantic_object=Summary)
    
    @staticmethod
    def create_ice_breaker_parser() -> PydanticOutputParser:
        """Create a parser for IceBreaker objects."""
        return PydanticOutputParser(pydantic_object=IceBreaker)
    
    @staticmethod
    def create_topics_of_interest_parser() -> PydanticOutputParser:
        """Create a parser for TopicOfInterest objects."""
        return PydanticOutputParser(pydantic_object=TopicOfInterest)


# Create common parsers for convenience
summary_parser = OutputParserFactory.create_summary_parser()
ice_breaker_parser = OutputParserFactory.create_ice_breaker_parser()
topics_of_interest_parser = OutputParserFactory.create_topics_of_interest_parser() 