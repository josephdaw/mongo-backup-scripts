"""Module to copy Staging to Local MongoDB.
This will copy the "staging" database down from the MongoDB Cloud. 
It will then restore that into the local MongoDB instance as "utm-staging"."""

# %% Import required modules
import os
import sys

from dotenv import load_dotenv

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.backup import create_backup
from scripts.restore import restore_backup

# %% Load environment variables from .env file
load_dotenv()

# Load configuration from environment variables
backup_mongodb_uri = os.getenv("UTM_MAIN_STAGING")
restore_mongodb_uri = os.getenv("MONGODB_URI_LOCAL")
backup_directory = os.getenv("BACKUP_DIRECTORY")

# Check if all required environment variables are set
if not backup_mongodb_uri:
    raise ValueError("backup_mongodb_uri environment variable is not set.")
if not restore_mongodb_uri:
    raise ValueError("restore_mongodb_uri environment variable is not set.")
if not backup_directory:
    raise ValueError("backup_directory environment variable is not set.")


def backup_staging_to_local():
    """Back up the staging database from MongoDB Cloud to a local directory."""
    create_backup(backup_mongodb_uri, "staging", backup_directory)


def restore_staging_to_local():
    """Restore the staging database from a local backup to the local MongoDB instance."""
    restore_backup(restore_mongodb_uri, "utm-staging", backup_directory, "staging")


if __name__ == "__main__":
    # Back up the staging database
    backup_staging_to_local()

    # Restore the staging database
    restore_staging_to_local()
