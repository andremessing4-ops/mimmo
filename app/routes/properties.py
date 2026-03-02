from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Property

router = APIRouter(prefix="/properties")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_properties(db: Session = Depends(get_db)):
    return db.query(Property).all()