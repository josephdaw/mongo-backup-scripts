# Mongo Database Backup Scripts

This repository contains scripts to backup and restore a MongoDB database.

## Setup

It is recommended to create a virtual environment to install the required dependencies. To create a virtual environment, run the following command:

```bash
python3 -m venv <environment-name>
```

For example:

```bash
python3 -m venv .venv
```

To activate the virtual environment, run one of the following commands:

- on MacOS/Linux:

  ```bash
  source <environment-name>/bin/activate
  ```

  For example:

  ```bash
  source .venv/bin/activate
  ```

- on Windows:
  ```bash
  <environment-name>\Scripts\activate
  ```
  For example:
  ```bash
  .venv\Scripts\activate
  ```

To install the required dependencies, run the following command:

```bash
pip install -r requirements.txt
```

## Configuration

## Backup

The backup script is a bash script that uses the `mongodump` command to backup a MongoDB database. The script takes the following parameters:

- `--host`: The host of the MongoDB database.
- `--port`: The port of the MongoDB database.
- `--db`: The name of the database to backup.
- `--out`: The directory where the backup will be stored.

Example usage:

```bash
./backup.sh --host localhost --port 27017 --db mydb --out /path/to/backup
```

## Restore

The restore script is a bash script that uses the `mongorestore` command to restore a MongoDB database from a backup. The script takes the following parameters:

- `--host`: The host of the MongoDB database.
- `--port`: The port of the MongoDB database.
- `--db`: The name of the database to restore.
- `--dir`: The directory where the backup is stored.

Example usage:

```bash
./restore.sh --host localhost --port 27017 --db mydb --dir /path/to/backup
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
