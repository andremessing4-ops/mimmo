from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.database import SessionLocal
from app.models import Payment, User
from app.services.orange_money import create_orange_payment

router = APIRouter(prefix="/payments", tags=["Payments"])

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
# INITIATE PAYMENT
# ==========================
@router.post("/orange")
def initiate_orange_payment(user_id: int, amount: int, phone: str, db: Session = Depends(get_db)):

    # Appel service Orange Money
    response = create_orange_payment(amount, phone)

    # Sauvegarde en base
    payment = Payment(
        user_id=user_id,
        amount=amount,
        transaction_id=response.get("transaction_id", "TEMP_ID"),
        status="pending"
    )

    db.add(payment)
    db.commit()

    return {
        "message": "Payment initiated",
        "orange_response": response
    }

# ==========================
# VERIFY PAYMENT
# ==========================
@router.get("/verify/{transaction_id}")
def verify_payment(transaction_id: str, db: Session = Depends(get_db)):

    payment = db.query(Payment).filter(
        Payment.transaction_id == transaction_id
    ).first()

    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    return {
        "transaction_id": transaction_id,
        "status": payment.status
    }