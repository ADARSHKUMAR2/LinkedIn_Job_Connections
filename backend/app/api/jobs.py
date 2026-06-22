from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, Field

from app.core.database import get_db
from app.models.job import JobListing
from app.services.job_scraper import fetch_and_sync_jobs  # Reusing your existing crawler function

router = APIRouter(
    prefix="/api/jobs",
    tags=["Job Listings"]
)

# --- Pydantic Schemas ---
class JobResponse(BaseModel):
    id: int
    job_id: str
    title: str
    company: str
    location: Optional[str]
    apply_link: Optional[str]

    class Config:
        from_attributes = True

class ScrapeRequest(BaseModel):
    search_query: str = Field(default="Software Engineer", example="AI ML Engineer")
    location: str = Field(default="India", example="Gurugram")


# --- Endpoint Controllers ---
@router.get("/", response_model=List[JobResponse])
def get_all_jobs(db: Session = Depends(get_db)):
    """Fetch all active tracked job listings inside your Supabase instance."""
    return db.query(JobListing).all()

@router.post("/scrape", status_code=status.HTTP_202_ACCEPTED)
def trigger_job_scrape(payload: ScrapeRequest, background_tasks: BackgroundTasks):
    """
    Triggers the JSearch external crawler script as an asynchronous background task 
    so the API doesn't hang or time out while downloading entries.
    """
    try:
        # BackgroundTasks runs this concurrently without blocking the main event loop
        background_tasks.add_task(
            fetch_and_sync_jobs, 
            search_query=payload.search_query, 
            location=payload.location
        )
        return {"status": "processing", "message": f"Scrape job initialized for '{payload.search_query}' in '{payload.location}'"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to cue up scraper: {str(e)}"
        )