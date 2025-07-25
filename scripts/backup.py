"""Module to create a backup of a MongoDB database."""

import os
import subprocess
import logging
from typing import Optional

from dotenv import load_dotenv


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_backup(
    mongodb_uri: str,
    database_name: str,
    backup_directory: str,
    timeout: Optional[int] = 300
) -> bool:
    """Create a backup of a MongoDB database.
    
    Args:
        mongodb_uri: MongoDB connection string
        database_name: Name of database to backup
        backup_directory: Directory to store backup files
        timeout: Command timeout in seconds (default: 300)
        
    Returns:
        bool: True if backup successful, False otherwise
        
    Raises:
        subprocess.CalledProcessError: If mongodump command fails
        subprocess.TimeoutExpired: If backup takes longer than timeout
    """
    logger.info(f"Starting backup of database '{database_name}'")
    
    try:
        # Ensure backup directory exists
        os.makedirs(backup_directory, exist_ok=True)
        logger.info(f"Backup directory created: {backup_directory}")

        # Create backup with timeout and error handling
        result = subprocess.run(
            [
                "mongodump",
                "--uri",
                mongodb_uri,
                "--db",
                database_name,
                "--out=" + backup_directory,
            ],
            check=True,
            timeout=timeout,
            capture_output=True,
            text=True
        )
        
        if result.stderr:
            logger.warning(f"Backup warnings: {result.stderr}")
        
        logger.info(f"Backup completed successfully for {database_name}")
        return True
        
    except subprocess.TimeoutExpired as e:
        logger.error(f"Backup timed out after {timeout} seconds: {e}")
        raise
    except subprocess.CalledProcessError as e:
        logger.error(f"Backup failed with exit code {e.returncode}: {e.stderr}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during backup: {e}")
        raise


# Example usage
if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()

    # Load configuration from environment variables
    env_mongodb_uri = os.getenv("BACKUP_MONGODB_URI")
    env_database_name = os.getenv("BACKUP_DATABASE_NAME")
    env_backup_directory = os.getenv("BACKUP_DIRECTORY")
    env_backup_filename_template = os.getenv("BACKUP_FILENAME")

    # Check if all required environment variables are set
    if not env_mongodb_uri:
        raise ValueError("BACKUP_MONGODB_URI environment variable is not set.")
    if not env_database_name:
        raise ValueError("BACKUP_DATABASE_NAME environment variable is not set.")
    if not env_backup_directory:
        raise ValueError("BACKUP_DIRECTORY environment variable is not set.")
    if not env_backup_filename_template:
        raise ValueError("BACKUP_FILENAME environment variable is not set.")

    create_backup(env_mongodb_uri, env_database_name, env_backup_directory)
