from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from pkg.database.alchemy import AlChemy
from dotenv import load_dotenv, find_dotenv
from pkg.database import DatabaseConfig
from app.entity import Base
import os

try:
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)
except Exception as e:
    print("Error load env: ", e)
    exit(0)

configMigration = DatabaseConfig(
        dbname=os.getenv("DB_MIGRATION_NAME"),
        user=os.getenv("DB_MIGRATION_USER"),
        password=os.getenv("DB_MIGRATION_PASSWORD"),
        host=os.getenv("DB_MIGRATION_HOST"),
        port=os.getenv("DB_MIGRATION_PORT"),
    )

alchemy = AlChemy()
connstr = alchemy.connection_setup_sync(configMigration, driver=os.environ.get("DB_DRIVER", "postgres"))
# engine = alchemy.async_engine(config=configMigration, driver=os.environ.get("DB_DRIVER", "postgres"))


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
config.set_main_option('sqlalchemy.url', connstr)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
