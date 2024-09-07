"""Module to create a backup of a MongoDB database."""

import os
import subprocess

from dotenv import load_dotenv


def create_backup(
    mongodb_uri,
    database_name,
    backup_directory,
):
    """Create a backup of a MongoDB database."""

    # Ensure backup directory exists
    os.makedirs(backup_directory, exist_ok=True)

    # Create backup
    subprocess.run(
        [
            "mongodump",
            "--uri",
            mongodb_uri,
            "--db",
            database_name,
            "--out=" + backup_directory,
        ],
        check=True,
    )

    print(f"Backup completed for {database_name}")


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
