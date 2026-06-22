import os
import sys
import requests
from dotenv import load_dotenv
from sqlalchemy.exc import IntegrityError
from app.core.database import SessionLocal
from app.models.job import JobListing
from sqlalchemy.dialects.postgresql import insert

# Load environmental state keys
load_dotenv(os.path.join(os.path.dirname(__file__), "../../.env"))

RAPID_API_KEY = os.getenv("RAPID_API_KEY")
if not RAPID_API_KEY:
    raise ValueError("CRITICAL ERROR: RAPID_API_KEY environmental variable is missing from your configuration.")

def fetch_and_sync_jobs(search_query: str = "Software Engineer", location: str = "India"):
    """
    Queries the external JSearch gateway via RapidAPI, parses incoming 
    payload frames, and syncs data idempotently into Supabase.
    """
    url = "https://jsearch.p.rapidapi.com/search"
    
    # Retrieve tokens from runtime environment
    rapid_api_key = os.getenv("RAPID_API_KEY")
    if not rapid_api_key:
        print("❌ CRITICAL ERROR: 'RAPID_API_KEY' is missing from your .env environment variables.", file=sys.stderr)
        return

    headers = {
        "X-RapidAPI-Key": rapid_api_key,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }
    
    # Query structure targeted at highly specialized developer roles
    querystring = {
        "query": f"{search_query} in {location}", 
        "num_pages": "1",
        "date_posted": "all"
    }
    
    db = SessionLocal()
    
    try:
        print(f"📡 Dispatching HTTP request to JSearch gateway: [{search_query}] in [{location}]...")
        
        # Extended timeout set to 30s to mitigate external gateway bottlenecks safely
        response = requests.get(url, headers=headers, params=querystring, timeout=30)
        response.raise_for_status()
        
        payload = response.json()
        job_records = payload.get("data", [])
        
        print(f"📦 JSearch data chunk returned. Processing {len(job_records)} payload rows...")
        
        sync_count = 0
        for raw_job in job_records:
            job_platform_id = raw_job.get("job_id")
            if not job_platform_id:
                continue
            
            # Format city, state, country into a unified string schema matching your data layout
            city = raw_job.get("job_city")
            state = raw_job.get("job_state")
            country = raw_job.get("job_country", "IN")
            
            location_components = [c for c in [city, state, country] if c]
            formatted_location = ", ".join(location_components) if location_components else "Remote"

            # 1. Prepare raw insert mapping
            insert_stmt = insert(JobListing).values(
                job_id=job_platform_id,
                title=raw_job.get("job_title", "Untitled Position"),
                company=raw_job.get("employer_name", "Unknown Corporate Entity"),
                location=formatted_location,
                apply_link=raw_job.get("job_apply_link")
            )
            
            # 2. Convert declaration into an Idempotent Upsert pattern
            # If the job_id unique key index exists, override metrics instead of raising an IntegrityError
            upsert_stmt = insert_stmt.on_conflict_do_update(
                index_elements=['job_id'],
                set_={
                    "title": insert_stmt.excluded.title,
                    "company": insert_stmt.excluded.company,
                    "location": insert_stmt.excluded.location,
                    "apply_link": insert_stmt.excluded.apply_link
                }
            )
            
            db.execute(upsert_stmt)
            sync_count += 1
            
        # Safely commit bulk transformations inside a singular database transaction window
        db.commit()
        print(f"✅ State Sync Finished: {sync_count} rows verified and merged cleanly into Supabase tables.")
        
    except requests.exceptions.Timeout:
        print("❌ HTTP ROUTING FAILURE: Connection to RapidAPI timed out (threshold 30s). Try again.", file=sys.stderr)
    except requests.exceptions.RequestException as req_err:
        print(f"❌ REQ ENGINE ERROR: Unable to contact RapidAPI platform: {req_err}", file=sys.stderr)
    except Exception as db_err:
        db.rollback()
        print(f"❌ STORAGE TRANSACTION ROLLBACK: Pipeline encountered database engine error: {db_err}", file=sys.stderr)
    finally:
        db.close()

# Local Sandbox Test Access Hook
if __name__ == "__main__":
    print("🧪 Running local sandbox scraper routine initialization...")
    fetch_and_sync_jobs(search_query="AI ML Engineer", location="Remote")