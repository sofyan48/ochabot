import os, uvicorn, argparse
from pkg import utils
from dotenv import load_dotenv
from config.logger import logging_config
from alembic import command
from alembic.config import Config

load_dotenv()
    

def migrate():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="subcommand", help="All Command")
    migrate_up_parser = subparsers.add_parser("up", help="Running migrate")
    migrate_create_parser = subparsers.add_parser("create", help="Create migrate")
    migrate_down_parser = subparsers.add_parser("down", help="Downgrade migrate")
    migrate_create_parser.add_argument("migration_name", help="Nama untuk migrasi baru")
    migrate_down_parser.add_argument("migration_revision", help="Migrate revision")
    migrate_up_parser.add_argument("migration_revision", help="Migrate revision")
    args = parser.parse_args()
    alembic_cfg = Config("alembic.ini")
    
    print(args.subcommand)

    if args.subcommand == "up":
        migrate_revision = args.migration_revision
        command.upgrade(alembic_cfg, migrate_revision)
        exit(0)

    if args.subcommand == "create":
        migration_name = args.migration_name
        command.revision(alembic_cfg, message=migration_name, autogenerate=False)  # Membuat migrasi baru
        exit(0)

    if args.subcommand == "down":
        migrate_revision = args.migration_revision
        command.downgrade(alembic_cfg, migrate_revision)
        exit(0)

    
def http():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="Perintah yang ingin Anda jalankan")
    args = parser.parse_args()

    if args.command == "serve":
        is_reload = False
        if utils.environment_transform() == 'loc':
            is_reload = True
        uvicorn.run(
            app="app:app",
            host=os.getenv("APP_HOST", "0.0.0.0"),
            port=int(os.getenv("APP_PORT", "8080")),
            reload=is_reload,
            log_config=logging_config
        )
        exit(0)

def main():
    http()
