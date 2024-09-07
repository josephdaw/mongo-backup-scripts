"""Module to restore a MongoDB backup."""

# %% Import required modules

import os
import subprocess

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load configuration from environment variables
restore_mongodb_uri = os.getenv("RESTORE_MONGODB_URI")
restore_database_name = os.getenv("RESTORE_DATABASE_NAME")
backup_database_name = os.getenv("BACKUP_DATABASE_NAME")
backup_directory = os.getenv("BACKUP_DIRECTORY")

# Check if all required environment variables are set
if not restore_mongodb_uri:
    raise ValueError("RESTORE_MONGODB_URI environment variable is not set.")
if not restore_database_name:
    raise ValueError("RESTORE_DATABASE_NAME environment variable is not set.")
if not backup_directory:
    raise ValueError("BACKUP_DIRECTORY environment variable is not set.")

# List available backups
backups = sorted(os.listdir(backup_directory))
if not backups:
    print("No backups found.")
    exit(1)

# Select the most recent backup
backup_filename = backups[-1]
backup_path = os.path.join(backup_directory, backup_filename)

restore_path = os.path.join(restore_mongodb_uri, restore_database_name)

# Restore backup
try:
    result = subprocess.run(
        [
            "mongorestore",
            "--uri=" + restore_path,
            backup_path,
            # "--gzip",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    print(result.stderr)
    print(f"Restore completed: {backup_path}")
except subprocess.CalledProcessError as e:
    print(f"Error during restore: {e}")
    print(e.stdout)
    print(e.stderr)

# %%
