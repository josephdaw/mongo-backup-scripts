"""Module to create a backup of a MongoDB database."""

# %% Import required modules
import os
import subprocess
from datetime import datetime

from dotenv import load_dotenv

# %% Load environment variables from .env file
# Load environment variables from .env file
load_dotenv()

# Load configuration from environment variables
mongodb_uri = os.getenv("BACKUP_MONGODB_URI")
database_name = os.getenv("BACKUP_DATABASE_NAME")
backup_directory = os.getenv("BACKUP_DIRECTORY")
backup_filename = (
    os.getenv("BACKUP_FILENAME")
    .replace("$(name)", database_name)
    .replace("$(date +%Y%m%d%H%M%S)", datetime.now().strftime("%Y%m%d%H%M%S"))
)

# Ensure backup directory exists
os.makedirs(backup_directory, exist_ok=True)

# Create backup
backup_path = os.path.join(backup_directory, backup_filename)
subprocess.run(
    [
        "mongodump",
        "--uri",
        mongodb_uri,
        "--db",
        database_name,
        "--out=" + backup_directory,
        # "--gzip",
    ],
    check=True,
)

print(f"Backup completed for {database_name}")

# %%
