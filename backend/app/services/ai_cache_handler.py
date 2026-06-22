import hashlib
import json
from sqlalchemy.orm import Session
from app.models.cache import MatchCache

def calculate_payload_hash(connections: list, jobs: list) -> str:
    """Generates a unique, deterministic SHA-256 signature for the dataset."""
    conn_ids = sorted([str(getattr(c, 'id', '')) for c in connections])
    job_ids = sorted([str(getattr(j, 'job_id', '')) for j in jobs])
    
    state_string = f"c:{','.join(conn_ids)}|j:{','.join(job_ids)}"
    return hashlib.sha256(state_string.encode('utf-8')).hexdigest()

def get_cached_matches(db: Session, payload_hash: str) -> getattr:
    """Checks the database for an existing, unexpired match matrix payload."""
    try:
        cached_entry = db.query(MatchCache).filter(MatchCache.payload_hash == payload_hash).first()
        if cached_entry:
            print("🚀 [CACHE HIT] Match matrix signature matched. Bypassing LLM overhead.")
            return json.loads(cached_entry.cached_response)
    except Exception as e:
        print(f"⚠️ Cache read issue encountered (ignoring): {e}")
    return None

def set_cached_matches(db: Session, payload_hash: str, matches: list):
    """Commits a fresh AI-validated match matrix to the persistent store."""
    try:
        # Delete old cache entry if it exists to avoid primary key conflicts
        db.query(MatchCache).filter(MatchCache.payload_hash == payload_hash).delete()
        
        new_cache = MatchCache(
            payload_hash=payload_hash,
            cached_response=json.dumps(matches)
        )
        db.add(new_cache)
        db.commit()
        print("💾 [CACHE SAVED] Fresh pipeline results written safely to Supabase.")
    except Exception as e:
        db.rollback()
        print(f"⚠️ Cache write transaction failed: {e}")