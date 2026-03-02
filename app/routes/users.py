from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User
from app.auth import hash_password

router = APIRouter(prefix="/users")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(nom: str, email: str, password: str, ville: str, telephone: str, db: Session = Depends(get_db)):

    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    user = User(
        nom=nom,
        email=email,
        password=hash_password(password),
        ville=ville,
        telephone=telephone
    )

    db.add(user)
    db.commit()

    return {"message": "User created"}