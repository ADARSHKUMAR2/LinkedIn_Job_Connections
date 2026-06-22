import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from app.core.database import Base

class MatchCache(Base):
    __tablename__ = "match_cache"

    id = Column(Integer, primary_key=True, index=True)
    # A unique MD5/SHA256 hash representing the exact payload signature sent to the AI
    payload_hash = Column(String, unique=True, index=True, nullable=False)
    # The stringified JSON response returned by the LLM
    cached_response = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)