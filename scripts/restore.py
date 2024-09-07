import os
import subprocess


def restore_backup(uri, database_name, backup_directory):
    """Restore a MongoDB database from a backup."""
    # List available backups
    backups = sorted(os.listdir(backup_directory))
    if not backups:
        print("No backups found.")
        return

    # Select the most recent backup
    backup_filename = backups[-1]
    backup_path = os.path.join(backup_directory, backup_filename)

    print(f"Selected backup file: {backup_path}")

    # Restore backup using --nsInclude
    try:
        result = subprocess.run(
            [
                "mongorestore",
                "--uri",
                uri,
                "--nsInclude",
                f"{database_name}.*",
                "--archive=" + backup_path,
                "--gzip",
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
