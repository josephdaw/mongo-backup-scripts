"""Module to restore a MongoDB database from a backup."""

import os
import subprocess


def restore_backup(
    uri, restored_database_name, backup_directory, backed_up_database_name
):
    """Restore a MongoDB database from a backup."""
    restore_path = os.path.join(uri, restored_database_name)
    backup_path = os.path.join(backup_directory, backed_up_database_name)

    # Restore backup
    try:
        result = subprocess.run(
            ["mongorestore", "--uri=" + restore_path, backup_path],
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
