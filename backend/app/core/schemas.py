# ==========================================
# 🆕 PYDANTIC SCHEMAS FOR STRUCTURED VALIDATION
# ==========================================

from pydantic import BaseModel, Field
from typing import List, Optional


class MatchInputSchema(BaseModel):
    """Ensures input data conforms to expectations before transmission."""
    connections: List[dict] = Field(..., description="List of processed LinkedIn contacts containing id, name, company, position.")
    jobs: List[dict] = Field(..., description="List of active job descriptions containing id, title, company, location.")

class MatchRecord(BaseModel):
    """The individual match layout pattern expected from the AI."""
    job_id: int = Field(..., description="The unique database ID key of the active job record.")
    connection_id: int = Field(..., description="The unique database ID key of the matched LinkedIn person.")
    reason: str = Field(..., description="Short explanation of semantic alignment (e.g., entity overlap or subsidiary link).")

class SemanticMatchResult(BaseModel):
    """Enforces that the overall AI response object matches a strict, typed list structure."""
    matches: List[MatchRecord] = Field(default_factory=list, description="Array collections containing verified relational matches.")

class MatcherFilterConfig(BaseModel):
    """Optional user-defined criteria to scope down the matchmaking sweep matrix dynamically."""
    target_location: Optional[str] = Field(None, description="Filter jobs by specific city/country (e.g., 'Gurugram', 'Remote').")
    target_company: Optional[str] = Field(None, description="Explicitly search for matches against a single target employer.")
    min_connections: int = Field(default=1, description="Minimum connections threshold before a job is considered.")