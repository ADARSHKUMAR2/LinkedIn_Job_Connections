from sqlalchemy import Column, Integer, String, DateTime, func, UniqueConstraint
from app.core.database import Base

class LinkedInConnection(Base):
    __tablename__ = "linkedin_connections"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    company = Column(String(255), index=True, nullable=True)
    position = Column(String(255), nullable=True)
    connected_on = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint('first_name', 'last_name', 'company', 'position', name='_connection_uc'),
    )