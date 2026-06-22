import sys
from app.core.schemas import MatchInputSchema, MatcherFilterConfig  
from app.services.ai_engine import execute_llm_matchmaking

def calculate_matches(db, user_config: MatcherFilterConfig = None):
    """
    Service Layer: Fetches database elements dynamically based on user filters,
    and passes scoped arrays to the isolated AI engine wrapper script.
    """
    from app.models.connection import LinkedInConnection
    from app.models.job import JobListing

    # If no config is passed from the router, instantiate an empty default filter state
    if user_config is None:
        user_config = MatcherFilterConfig()

    print("📡 Service Layer: Initializing filtered query hooks on Supabase...")
    
    # 1. Build dynamic queries using SQLAlchemy filters
    job_query = db.query(JobListing)
    connection_query = db.query(LinkedInConnection)

    # Apply Location Filter if provided by the user input parameter
    if user_config.target_location:
        print(f"🔍 Filtering target job options scoped to location: '{user_config.target_location}'")
        job_query = job_query.filter(JobListing.location.ilike(f"%{user_config.target_location}%"))

    # Apply Company Filter if looking for an explicit employer pipeline path
    if user_config.target_company:
        print(f"🏢 Scoping network elements down to employer matching keyword: '{user_config.target_company}'")
        job_query = job_query.filter(JobListing.company.ilike(f"%{user_config.target_company}%"))
        connection_query = connection_query.filter(LinkedInConnection.company.ilike(f"%{user_config.target_company}%"))

    connections = connection_query.all()
    jobs = job_query.all()

    if not connections or not jobs:
        print("⚠️ Matchmaking skipped: No records matched your filter settings in the database.")
        return []

    # 2. Package database records into structured dictionary format
    network_data = [
        {"id": c.id, "name": f"{c.first_name} {c.last_name}", "company": c.company, "position": c.position}
        for c in connections if c.company
    ]
    job_data = [
        {"id": j.id, "title": j.title, "company": j.company, "location": j.location, "apply_link": j.apply_link}
        for j in jobs if j.company
    ]

    # 3. Validate overall payload framing using standard Pydantic models
    try:
        validated_input = MatchInputSchema(connections=network_data, jobs=job_data)
    except Exception as validation_err:
        print(f"❌ Input Validation Failed: {validation_err}", file=sys.stderr)
        return []

    # 4. Invoke our completely separated AI Engine executor script
    print("🧠 Invoking isolated AI engine wrapper module with scoped sub-matrix data payload...")
    try:
        parsed_response = execute_llm_matchmaking(validated_input)
    except Exception as err:
        print(f"❌ AI Engine Script Interruption: {err}. Falling back to basic loop...", file=sys.stderr)
        return calculate_matches_fallback(connections, jobs)

    # 5. Hydrate returned reference pointer integer indexes back into display names
    matched_results = []
    conn_dict = {c.id: c for c in connections}
    job_dict = {j.id: j for j in jobs}

    for match in parsed_response.matches:
        j_obj = job_dict.get(match.job_id)
        c_obj = conn_dict.get(match.connection_id)
        
        if j_obj and c_obj:
            matched_results.append({
                "Company": j_obj.company.upper(),
                "Target Role": j_obj.title,
                "Location": j_obj.location or "Remote / Unspecified",
                "Inside Contact": f"{c_obj.first_name} {c_obj.last_name}",
                "Contact Position": c_obj.position,
                "Application Link": j_obj.apply_link or "No Link Available"
            })
    
    return matched_results


def calculate_matches_fallback(connections, jobs):
    """Deterministic fallback algorithm tracking basic token substrings."""
    matched_results = []
    for job in jobs:
        for person in connections:
            if person.company and job.company and person.company.lower() in job.company.lower():
                matched_results.append({
                    "Company": job.company.upper(),
                    "Target Role": job.title,
                    "Location": job.location or "Remote / Unspecified",
                    "Inside Contact": f"{person.first_name} {person.last_name}",
                    "Contact Position": person.position,
                    "Application Link": job.apply_link or "No Link Available"
                })
    return matched_results

def run_matchmaker_loop():
    from app.core.database import SessionLocal
    db = SessionLocal()
    
    # 🆕 SIMULATE CUSTOM USER FILTERS:
    # Let's say a user only wants to inspect jobs located in 'Gurugram'
    test_filter = MatcherFilterConfig(target_location="Gurugram")
    
    matches = calculate_matches(db, user_config=test_filter)
    print(f"\n🎉 Filtered Sweep Completed! Found {len(matches)} AI-Validated Referral Pathways.")
    for idx, match in enumerate(matches, 1):
        print(f"   🎯 [{idx}] Match: {match['Inside Contact']} ({match['Contact Position']}) at {match['Company']} ({match['Location']})")
    db.close()

if __name__ == "__main__":
    run_matchmaker_loop()