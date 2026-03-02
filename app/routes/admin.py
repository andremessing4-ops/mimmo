from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.database import SessionLocal
from app.models import User, Payment

router = APIRouter(prefix="/admin", tags=["Admin"])

# ==========================
# DB DEPENDENCY
# ==========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================
# LIST USERS
# ==========================
@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

# ==========================
# APPROVE USER
# ==========================
@router.put("/approve/{user_id}")
def approve_user(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.approved = True
    user.subscription_expiry = datetime.utcnow() + timedelta(days=30)

    db.commit()

    return {"message": "User approved and subscription activated"}

# ==========================
# LIST PAYMENTS
# ==========================
@router.get("/payments")
def get_payments(db: Session = Depends(get_db)):
    return db.query(Payment).all()

# ==========================
# DASHBOARD STATISTICS
# ==========================
@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):

    total_users = db.query(User).count()
    total_payments = db.query(Payment).count()
    approved_users = db.query(User).filter(User.approved == True).count()

    return {
        "total_users": total_users,
        "approved_users": approved_users,
        "total_payments": total_payments
    }