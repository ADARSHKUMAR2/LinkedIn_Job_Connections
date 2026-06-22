from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel, Field, HttpUrl

from app.core.database import get_db
from app.models.connection import LinkedInConnection

router = APIRouter(
    prefix="/api/connections",
    tags=["LinkedIn Connections"]
)

# --- Pydantic Schemas for Request/Response Validation ---
class ConnectionBase(BaseModel):
    first_name: str = Field(..., example="Bob")
    last_name: str = Field(..., example="Miller")
    # profile_url: HttpUrl = Field(..., example="https://www.linkedin.com/in/bobmiller")
    company: str = Field(..., example="American Express")
    position: str = Field(..., example="VP of Engineering")

class ConnectionCreate(ConnectionBase):
    pass

class ConnectionResponse(ConnectionBase):
    id: int

    class Config:
        from_attributes = True


# --- Endpoint Controllers ---
@router.get("/", response_model=List[ConnectionResponse])
def get_all_connections(db: Session = Depends(get_db)):
    """Fetch all stored LinkedIn connections from the database."""
    return db.query(LinkedInConnection).all()

@router.post("/", response_model=ConnectionResponse, status_code=status.HTTP_201_CREATED)
def create_connection(payload: ConnectionCreate, db: Session = Depends(get_db)):
    """Manually add a new single LinkedIn connection path to the network registry."""
    # Check if connection already exists to avoid duplicates
    existing = db.query(LinkedInConnection).filter(
        LinkedInConnection.profile_url == str(payload.profile_url)
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A connection with this LinkedIn profile URL already exists."
        )
        
    db_connection = LinkedInConnection(
        first_name=payload.first_name,
        last_name=payload.last_name,
        profile_url=str(payload.profile_url),
        company=payload.company,
        position=payload.position
    )
    db.add(db_connection)
    db.commit()
    db.refresh(db_connection)
    return db_connection

@router.delete("/{connection_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_connection(connection_id: int, db: Session = Depends(get_db)):
    """Remove a LinkedIn connection by its primary database ID key."""
    connection = db.query(LinkedInConnection).filter(LinkedInConnection.id == connection_id).first()
    if not connection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Connection index {connection_id} not found."
        )
    db.delete(connection)
    db.commit()
    return