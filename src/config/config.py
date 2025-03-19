"""
Configuration module for the SearchAgent application.
Handles loading environment variables and other configuration settings.
"""
import os
from pathlib import Path
from typing import Dict, Any, Optional
import yaml
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ConfigurationManager:
    """
    Manages configuration settings for the application.
    Follows the Singleton design pattern.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigurationManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize configuration settings."""
        self.config: Dict[str, Any] = {}
        self._load_env_variables()
        
    def _load_env_variables(self):
        """Load environment variables into the configuration."""
        # API Keys
        self.config["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")
        self.config["SCRAPIN_API_KEY"] = os.getenv("SCRAPIN_API_KEY", "")
        self.config["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY", "")
        self.config["TWITTER_API_KEY"] = os.getenv("TWITTER_API_KEY", "")
        self.config["TWITTER_API_SECRET"] = os.getenv("TWITTER_API_SECRET", "")
        self.config["TWITTER_ACCESS_TOKEN"] = os.getenv("TWITTER_ACCESS_TOKEN", "")
        self.config["TWITTER_ACCESS_SECRET"] = os.getenv("TWITTER_ACCESS_SECRET", "")
        
        # LangChain Tracing
        self.config["LANGCHAIN_TRACING_V2"] = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
        self.config["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY", "")
        self.config["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT", "ice_breaker")
        
        # Application Settings
        self.config["DEBUG"] = os.getenv("DEBUG", "false").lower() == "true"
        self.config["HOST"] = os.getenv("HOST", "0.0.0.0")
        self.config["PORT"] = int(os.getenv("PORT", "5000"))
        
        # Device settings for PyTorch
        self.config["DEVICE"] = self._determine_device()
    
    def _determine_device(self) -> str:
        """Determine the best available device for PyTorch."""
        import torch
        if torch.cuda.is_available():
            return "cuda"
        elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            return "mps"  # For Mac M1/M2 GPU support
        else:
            return "cpu"
    
    def load_yaml_config(self, config_path: str) -> None:
        """
        Load configuration from a YAML file.
        
        Args:
            config_path: Path to the YAML configuration file
        """
        config_file = Path(config_path)
        if config_file.exists():
            with open(config_file, "r") as f:
                yaml_config = yaml.safe_load(f)
                if yaml_config:
                    self.config.update(yaml_config)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key: The configuration key
            default: Default value if key is not found
            
        Returns:
            The configuration value
        """
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value.
        
        Args:
            key: The configuration key
            value: The value to set
        """
        self.config[key] = value
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to a dictionary.
        
        Returns:
            Dictionary of configuration values
        """
        return self.config.copy()
    
    def validate_required_keys(self, required_keys: list) -> bool:
        """
        Validate that all required keys are present and have values.
        
        Args:
            required_keys: List of required configuration keys
            
        Returns:
            True if all required keys have values, False otherwise
        """
        for key in required_keys:
            if not self.config.get(key):
                return False
        return True

# Create a global instance of the configuration manager
config = ConfigurationManager() 