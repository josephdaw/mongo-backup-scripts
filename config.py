"""Configuration management and validation for MongoDB backup scripts."""

import os
import logging
from urllib.parse import urlparse
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class ConfigurationError(Exception):
    """Raised when configuration is invalid or missing."""
    pass


def validate_mongodb_uri(uri: str) -> bool:
    """Validate MongoDB connection string format."""
    try:
        parsed = urlparse(uri)
        return parsed.scheme in ['mongodb', 'mongodb+srv'] and bool(parsed.netloc)
    except Exception:
        return False


def validate_required_tools() -> Dict[str, bool]:
    """Check if required MongoDB tools are available."""
    tools = {
        'mongodump': False,
        'mongorestore': False
    }
    
    for tool in tools:
        try:
            import subprocess
            result = subprocess.run([tool, '--version'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5)
            tools[tool] = result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            tools[tool] = False
    
    return tools


class Config:
    """Configuration manager for MongoDB backup operations."""
    
    def __init__(self):
        self.environments = {
            'production': os.getenv('UTM_MAIN_PRODUCTION'),
            'staging': os.getenv('UTM_MAIN_STAGING'), 
            'dev': os.getenv('UTM_MAIN_DEV'),
            'local': os.getenv('MONGODB_URI_LOCAL')
        }
        self.backup_directory = os.getenv('BACKUP_DIRECTORY')
        self._validate_config()
    
    def _validate_config(self):
        """Validate configuration on initialization."""
        # Check backup directory
        if not self.backup_directory:
            raise ConfigurationError("BACKUP_DIRECTORY environment variable not set")
        
        # Validate MongoDB URIs
        for env_name, uri in self.environments.items():
            if uri and not validate_mongodb_uri(uri):
                logger.warning(f"Invalid MongoDB URI format for {env_name}")
        
        # Check MongoDB tools
        tools = validate_required_tools()
        missing_tools = [tool for tool, available in tools.items() if not available]
        if missing_tools:
            raise ConfigurationError(f"Missing required MongoDB tools: {', '.join(missing_tools)}")
    
    def get_uri(self, environment: str) -> str:
        """Get MongoDB URI for specified environment."""
        if environment not in self.environments:
            raise ConfigurationError(f"Unknown environment: {environment}")
        
        uri = self.environments[environment]
        if not uri:
            raise ConfigurationError(f"No URI configured for environment: {environment}")
        
        return uri
    
    def get_backup_directory(self) -> str:
        """Get backup directory path."""
        return self.backup_directory
    
    def list_environments(self) -> list:
        """List available environments."""
        return [env for env, uri in self.environments.items() if uri]


# Global config instance
config = Config()