import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Resolve workspace environment paths
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("CRITICAL ERROR: DATABASE_URL environment variable is missing.")

# Fix protocol syntax for modern async-compatible drivers if necessary
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Initialize SQL Engine with production pool sizing configuration
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True  # Guarantees session resilience against cloud disconnects
)

# Shared Session Factory context
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base model mapping context for tables
Base = declarative_base()

def get_db():
    """Provides a transactional scope for database operations."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()