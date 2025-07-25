"""Module to restore a MongoDB database from a backup."""

import os
import subprocess
import logging
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def restore_backup(
    uri: str, 
    restored_database_name: str, 
    backup_directory: str, 
    backed_up_database_name: str,
    timeout: Optional[int] = 600
) -> bool:
    """Restore a MongoDB database from a backup.
    
    Args:
        uri: MongoDB connection string for restore destination
        restored_database_name: Name for the restored database
        backup_directory: Directory containing backup files
        backed_up_database_name: Name of the original backed up database
        timeout: Command timeout in seconds (default: 600)
        
    Returns:
        bool: True if restore successful, False otherwise
        
    Raises:
        subprocess.CalledProcessError: If mongorestore command fails
        subprocess.TimeoutExpired: If restore takes longer than timeout
        FileNotFoundError: If backup directory doesn't exist
    """
    logger.info(f"Starting restore of '{backed_up_database_name}' to '{restored_database_name}'")
    
    restore_path = os.path.join(uri, restored_database_name)
    backup_path = os.path.join(backup_directory, backed_up_database_name)
    
    # Validate backup path exists
    if not os.path.exists(backup_path):
        error_msg = f"Backup directory not found: {backup_path}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)

    try:
        result = subprocess.run(
            ["mongorestore", "--uri=" + restore_path, backup_path],
            check=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        if result.stdout:
            logger.info(f"Restore output: {result.stdout}")
        if result.stderr:
            logger.warning(f"Restore warnings: {result.stderr}")
            
        logger.info(f"Restore completed successfully: {backup_path}")
        return True
        
    except subprocess.TimeoutExpired as e:
        logger.error(f"Restore timed out after {timeout} seconds: {e}")
        raise
    except subprocess.CalledProcessError as e:
        logger.error(f"Restore failed with exit code {e.returncode}")
        if e.stdout:
            logger.error(f"Stdout: {e.stdout}")
        if e.stderr:
            logger.error(f"Stderr: {e.stderr}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during restore: {e}")
        raise
