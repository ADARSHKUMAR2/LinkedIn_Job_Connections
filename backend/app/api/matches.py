from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.core.database import get_db  # Assuming you have a standard get_db session dependency
from app.core.schemas import MatcherFilterConfig, OutreachDraftResult
from app.services.ai_matcher import calculate_matches
from app.services.ai_engine import execute_llm_outreach_draft

router = APIRouter(
    prefix="/api/matches",
    tags=["Matchmaking & Outreach"]
)

@router.post("/sweep", response_model=List[Dict[str, Any]])
def run_filtered_sweep(
    filters: MatcherFilterConfig, 
    db: Session = Depends(get_db)
):
    """
    Exposes the core database-filtering and semantic-matching pipeline over HTTP.
    Accepts optional json fields: target_location, target_company.
    """
    try:
        results = calculate_matches(db, user_config=filters)
        return results
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Matchmaker execution failure: {str(e)}"
        )

@router.post("/draft-outreach", response_model=OutreachDraftResult)
def generate_single_outreach(match_context: Dict[str, Any]):
    """
    Takes a single match result dictionary and commands the isolated 
    AI engine wrapper to generate structural outreach templates.
    """
    # Quick validation to ensure required context keys exist
    required_keys = ["Inside Contact", "Contact Position", "Company", "Target Role"]
    if not all(key in match_context for key in required_keys):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Missing essential tracking data. Context must include: {required_keys}"
        )
        
    try:
        draft = execute_llm_outreach_draft(match_context)
        return draft
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"LLM text drafting failed: {str(e)}"
        )