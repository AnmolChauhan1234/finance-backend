from logging.config import fileConfig
import os

from sqlalchemy import create_engine, pool
from alembic import context

from app.db.base import Base
from app.models import *

# Alembic Config
config = context.config

# Setup logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Get DB URL
database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise ValueError("DATABASE_URL is not set")

# Set DB URL for Alembic
config.set_main_option("sqlalchemy.url", database_url)

# Metadata for autogenerate
target_metadata = Base.metadata


# OFFLINE MODE
def run_migrations_offline() -> None:
    context.configure(
        url=database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# ONLINE MODE
def run_migrations_online() -> None:
    connectable = create_engine(
        database_url,
        poolclass=pool.NullPool,
        pool_pre_ping=True,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


# ENTRY POINT
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()