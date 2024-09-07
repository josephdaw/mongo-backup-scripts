"""Module to back up UTM staging to local MongoDB."""

# %% Import required modules
import os
import sys

from dotenv import load_dotenv

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts import create_backup  # pylint: disable=wrong-import-position

# %% Load environment variables from .env file
load_dotenv()

# Load configuration from environment variables
backup_mongodb_uri = os.getenv("MONGODB_URI_PROJECT0_CLUSTER0")
# backup_database_name = "utm-dev-v2"
backup_directory = os.getenv("BACKUP_DIRECTORY")

# Check if all required environment variables are set
if not backup_mongodb_uri:
    raise ValueError("backup_mongodb_uri environment variable is not set.")
# if not backup_database_name:
# raise ValueError("backup_database_name environment variable is not set.")
if not backup_directory:
    raise ValueError("backup_directory environment variable is not set.")

# %% Back up UTM Staging to Local MongoDB
create_backup(backup_mongodb_uri, "utm-dev-v2", backup_directory)
