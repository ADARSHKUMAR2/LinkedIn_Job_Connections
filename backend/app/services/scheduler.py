from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.services.job_scraper import fetch_and_sync_jobs

# Initialize a BackgroundScheduler instance
scheduler = BackgroundScheduler()

def start_automated_cron_jobs():
    """Configures and runs background cron loops within the app cluster context."""
    
    # 🆕 Task 1: Schedule the JSearch crawler to run automatically every night at 12:00 AM
    scheduler.add_job(
        fetch_and_sync_jobs,
        trigger=CronTrigger(hour=0, minute=0),
        kwargs={"search_query": "AI ML Engineer", "location": "Gurugram"},
        id="daily_jsearch_sync",
        name="Nightly sync of fresh job targets from RapidAPI",
        replace_existing=True
    )
    
    # 🧪 TEST CRON TASK (Optional Debug Tool):
    # Uncomment this block if you want to verify it fires immediately every 60 seconds
    
    scheduler.add_job(
        fetch_and_sync_jobs,
        trigger="interval",
        minutes=1,
        kwargs={"search_query": "Software Engineer", "location": "WFH"},
        id="test_short_interval",
        replace_existing=True
    )
    
    print("⏰  Scheduler Engine: Automated background cron loops initialized successfully.")
    scheduler.start()

def shutdown_automated_cron_jobs():
    """Cleanly terminates scheduler worker loops during server teardown."""
    print("⏰  Scheduler Engine: Shutting down worker threads...")
    scheduler.shutdown()