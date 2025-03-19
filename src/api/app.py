"""
Flask application for the SearchAgent.
Provides a web interface for generating ice breakers.
"""
import logging
import os
from typing import Dict, Any
from flask import Flask, render_template, request, jsonify
from SearchAgent.src.ice_breaker import IceBreakerService
from SearchAgent.src.config import config

# Set up logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class IceBreakerApp:
    """
    Flask application for the SearchAgent.
    Follows the Singleton design pattern.
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(IceBreakerApp, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize the application."""
        # Create the Flask application
        self.app = Flask(
            __name__, 
            template_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates"),
            static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
        )
        
        # Create the service
        self.ice_breaker_service = IceBreakerService(
            use_mock=config.get("USE_MOCK_DATA", False)
        )
        
        # Register routes
        self._register_routes()
    
    def _register_routes(self):
        """Register routes for the application."""
        self.app.add_url_rule("/", "index", self.index)
        self.app.add_url_rule("/process", "process", self.process, methods=["POST"])
        self.app.add_url_rule("/health", "health", self.health)
    
    def index(self):
        """
        Render the index page.
        
        Returns:
            Rendered index.html template
        """
        return render_template("index.html")
    
    def process(self):
        """
        Process a request to generate ice breakers.
        
        Returns:
            JSON response with ice breakers
            
        Raises:
            500: If there is an error generating ice breakers
        """
        try:
            name = request.form["name"]
            logger.info(f"Processing request for {name}")
            
            summary_and_facts, interests, ice_breakers, profile_pic_url = self.ice_breaker_service.ice_break_with(
                name=name
            )
            
            return jsonify(
                {
                    "summary_and_facts": summary_and_facts.to_dict(),
                    "interests": interests.to_dict(),
                    "ice_breakers": ice_breakers.to_dict(),
                    "picture_url": profile_pic_url,
                }
            )
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    def health(self):
        """
        Health check endpoint.
        
        Returns:
            JSON response with health status
        """
        return jsonify({"status": "ok"})
    
    def run(self, host: str = None, port: int = None, debug: bool = None):
        """
        Run the application.
        
        Args:
            host: Host to run the application on (defaults to config)
            port: Port to run the application on (defaults to config)
            debug: Whether to run in debug mode (defaults to config)
        """
        host = host or config.get("HOST", "0.0.0.0")
        port = port or config.get("PORT", 5000)
        debug = debug if debug is not None else config.get("DEBUG", False)
        
        logger.info(f"Starting application on {host}:{port} (debug={debug})")
        self.app.run(host=host, port=port, debug=debug)


# Create global application instance
app_instance = IceBreakerApp()


if __name__ == "__main__":
    app_instance.run() 