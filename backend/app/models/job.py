from sqlalchemy import Column, Integer, String, Text, DateTime, func, UniqueConstraint
from app.core.database import Base

class JobListing(Base):
    __tablename__ = "job_listings"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String(100), unique=True, index=True, nullable=False) # JSearch unique ID
    title = Column(String(255), nullable=False)
    company = Column(String(255), index=True, nullable=False)
    location = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    apply_link = Column(Text, nullable=True)
    posted_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint('company', 'title', name='_job_company_title_uc'),
    )