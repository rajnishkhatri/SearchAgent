"""
Main entry point for the SearchAgent application.
"""
import logging
import os
import sys

# Add the root directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import the application
from src.api.app import app_instance


def main():
    """Run the application."""
    try:
        app_instance.run()
    except Exception as e:
        logger.error(f"Error running application: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main() 