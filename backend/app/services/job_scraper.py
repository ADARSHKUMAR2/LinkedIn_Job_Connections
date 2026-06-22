import os
import sys
import requests
from dotenv import load_dotenv
from sqlalchemy.exc import IntegrityError
from app.core.database import SessionLocal
from app.models.job import JobListing

# Load environmental state keys
load_dotenv(os.path.join(os.path.dirname(__file__), "../../.env"))

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
if not RAPIDAPI_KEY:
    raise ValueError("CRITICAL ERROR: RAPIDAPI_KEY environmental variable is missing from your configuration.")

def fetch_and_sync_jobs(search_query: str = "Software Engineer", location: str = "United States", pages: int = 1):
    print("==================================================================")
    print(f"📡 Querying JSearch Gateway for: '{search_query}' in '{location}'")
    print("==================================================================")

    url = "https://jsearch.p.rapidapi.com/search"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }
    
    # Combined intent parameter matching what JSearch reads best
    full_query = f"{search_query} in {location}"
    
    params = {
        "query": full_query,
        "page": str(pages),
        "num_pages": "1",
        "date_posted": "week" # Restrict lookup to fresh positions posted this week
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
    except Exception as network_err:
        print(f"❌ HTTP ROUTING FAILURE: Unable to contact RapidAPI endpoint.\nDetails: {network_err}", file=sys.stderr)
        return

    job_records = data.get("data", [])
    if not job_records:
        print("⚠️  API Response returned a clean state but zero matching active roles.")
        return

    db = SessionLocal()
    added_jobs = 0
    duplicate_jobs = 0

    try:
        print(f"🚀 Found {len(job_records)} job payloads. Streaming metrics to Supabase...")
        for job in job_records:
            # Safely parse out only what our engine tracking tables need
            job_id = job.get("job_id")
            if not job_id:
                continue

            new_job = JobListing(
                job_id=job_id,
                title=job.get("job_title", "Unknown Role"),
                company=job.get("employer_name", "Unknown Company"),  
                location=f"{job.get('job_city', '')}, {job.get('job_state', '')} {job.get('job_country', '')}".strip(", "),
                description=job.get("job_description"),
                apply_link=job.get("job_apply_link")                  
            )

            try:
                db.add(new_job)
                db.commit()
                added_jobs += 1
            except IntegrityError:
                db.rollback()
                duplicate_jobs += 1
            except Exception:
                db.rollback()

        print("\n🎉 LIVE MARKET CAPTURE COMPLETE:")
        print(f"   💼 New Open Positions Ingested: {added_jobs}")
        print(f"   ⚠️  Skipped Duplicate Jobs:      {duplicate_jobs}")

    finally:
        db.close()
        print("==================================================================")

if __name__ == "__main__":
    # Test execution parameters to pull mock openings for HighLevel and Google matching our sample CSV entries
    fetch_and_sync_jobs(search_query="AI Engineer", location="India")