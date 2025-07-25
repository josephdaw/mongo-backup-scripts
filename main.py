#!/usr/bin/env python3
"""
Unified CLI interface for MongoDB backup and restore operations.

This script provides a centralized command-line interface for managing
MongoDB database backups and restores across different environments.
"""

import argparse
import sys
import logging
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

from config import config, ConfigurationError
from scripts.backup import create_backup
from scripts.restore import restore_backup

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def setup_argument_parser():
    """Set up command line argument parser."""
    parser = argparse.ArgumentParser(
        description="MongoDB backup and restore utility",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s backup --env production --database production
  %(prog)s restore --env local --database utm-production --source production
  %(prog)s sync --source staging --target local --target-db utm-staging
  %(prog)s list-envs
        """
    )
    
    subparsers = parser.add_subparsers(dest='action', help='Available actions')
    
    # Backup command
    backup_parser = subparsers.add_parser('backup', help='Create database backup')
    backup_parser.add_argument('--env', required=True, 
                              choices=config.list_environments(),
                              help='Source environment')
    backup_parser.add_argument('--database', required=True,
                              help='Database name to backup')
    backup_parser.add_argument('--timeout', type=int, default=300,
                              help='Backup timeout in seconds (default: 300)')
    
    # Restore command
    restore_parser = subparsers.add_parser('restore', help='Restore database from backup')
    restore_parser.add_argument('--env', required=True,
                               choices=config.list_environments(),
                               help='Target environment')
    restore_parser.add_argument('--database', required=True,
                               help='Target database name')
    restore_parser.add_argument('--source', required=True,
                               help='Source backup database name')
    restore_parser.add_argument('--timeout', type=int, default=600,
                               help='Restore timeout in seconds (default: 600)')
    
    # Sync command (backup + restore)
    sync_parser = subparsers.add_parser('sync', help='Sync database from source to target')
    sync_parser.add_argument('--source', required=True,
                            choices=[env for env in config.list_environments() if env != 'local'],
                            help='Source environment')
    sync_parser.add_argument('--target', default='local',
                            choices=config.list_environments(),
                            help='Target environment (default: local)')
    sync_parser.add_argument('--source-db', required=True,
                            help='Source database name')
    sync_parser.add_argument('--target-db', required=True,
                            help='Target database name')
    sync_parser.add_argument('--backup-timeout', type=int, default=300,
                            help='Backup timeout in seconds (default: 300)')
    sync_parser.add_argument('--restore-timeout', type=int, default=600,
                            help='Restore timeout in seconds (default: 600)')
    
    # List environments command
    subparsers.add_parser('list-envs', help='List available environments')
    
    return parser


def handle_backup(args):
    """Handle backup command."""
    try:
        source_uri = config.get_uri(args.env)
        backup_dir = config.get_backup_directory()
        
        logger.info(f"Starting backup: {args.env}/{args.database}")
        success = create_backup(
            mongodb_uri=source_uri,
            database_name=args.database,
            backup_directory=backup_dir,
            timeout=args.timeout
        )
        
        if success:
            logger.info("Backup completed successfully")
            return 0
        else:
            logger.error("Backup failed")
            return 1
            
    except Exception as e:
        logger.error(f"Backup error: {e}")
        return 1


def handle_restore(args):
    """Handle restore command."""
    try:
        target_uri = config.get_uri(args.env)
        backup_dir = config.get_backup_directory()
        
        logger.info(f"Starting restore: {args.source} -> {args.env}/{args.database}")
        success = restore_backup(
            uri=target_uri,
            restored_database_name=args.database,
            backup_directory=backup_dir,
            backed_up_database_name=args.source,
            timeout=args.timeout
        )
        
        if success:
            logger.info("Restore completed successfully")
            return 0
        else:
            logger.error("Restore failed")
            return 1
            
    except Exception as e:
        logger.error(f"Restore error: {e}")
        return 1


def handle_sync(args):
    """Handle sync command (backup + restore)."""
    try:
        source_uri = config.get_uri(args.source)
        target_uri = config.get_uri(args.target)
        backup_dir = config.get_backup_directory()
        
        logger.info(f"Starting sync: {args.source}/{args.source_db} -> {args.target}/{args.target_db}")
        
        # Step 1: Backup
        logger.info("Step 1: Creating backup")
        backup_success = create_backup(
            mongodb_uri=source_uri,
            database_name=args.source_db,
            backup_directory=backup_dir,
            timeout=args.backup_timeout
        )
        
        if not backup_success:
            logger.error("Backup failed, aborting sync")
            return 1
        
        # Step 2: Restore
        logger.info("Step 2: Restoring backup")
        restore_success = restore_backup(
            uri=target_uri,
            restored_database_name=args.target_db,
            backup_directory=backup_dir,
            backed_up_database_name=args.source_db,
            timeout=args.restore_timeout
        )
        
        if restore_success:
            logger.info("Sync completed successfully")
            return 0
        else:
            logger.error("Restore failed")
            return 1
            
    except Exception as e:
        logger.error(f"Sync error: {e}")
        return 1


def handle_list_envs(args):
    """Handle list-envs command."""
    print("Available environments:")
    for env in config.list_environments():
        print(f"  - {env}")
    return 0


def main():
    """Main entry point."""
    try:
        parser = setup_argument_parser()
        args = parser.parse_args()
        
        if not args.action:
            parser.print_help()
            return 1
        
        # Route to appropriate handler
        handlers = {
            'backup': handle_backup,
            'restore': handle_restore,
            'sync': handle_sync,
            'list-envs': handle_list_envs
        }
        
        handler = handlers.get(args.action)
        if handler:
            return handler(args)
        else:
            logger.error(f"Unknown action: {args.action}")
            return 1
            
    except ConfigurationError as e:
        logger.error(f"Configuration error: {e}")
        return 1
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())