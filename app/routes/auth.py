from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User
from app.auth import verify_password, create_access_token

router = APIRouter(prefix="/auth")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.email, "role": user.role})

    return {"access_token": token, "token_type": "bearer"}