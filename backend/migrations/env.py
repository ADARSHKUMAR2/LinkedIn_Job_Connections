import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# Ensure the backend directory is accessible to the python path loader
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import your application engine elements
from app.core.database import Base
# Import your database models so they register their structural footprints with Base.metadata
from app.models.connection import LinkedInConnection
from app.models.job import JobListing

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    load_dotenv(os.path.join(os.path.dirname(__file__), "../.env"))
    url = os.getenv("DATABASE_URL")
    
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode (Direct network push)."""
    load_dotenv(os.path.join(os.path.dirname(__file__), "../.env"))
    configuration = config.get_section(config.config_ini_section) or {}
    configuration["sqlalchemy.url"] = os.getenv("DATABASE_URL")
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()