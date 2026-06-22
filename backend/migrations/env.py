import os
from logging.config import fileConfig
from dotenv import load_dotenv
from alembic import context

# 1. Inherit core configuration and setup paths
from backend.app.core.database import Base

# Load environmental variables securely from runtime path
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 2. Wire target metadata metrics for autogenerate mapping support
target_metadata = Base.metadata

# 3. Dynamic connection string ingestion
db_url = os.getenv("DATABASE_URL")
if db_url:
    config.set_main_option("sqlalchemy.url", db_url)