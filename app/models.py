from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


# ==========================
# USER MODEL
# ==========================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    nom = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    telephone = Column(String, nullable=False)
    ville = Column(String, nullable=False)
    password = Column(String, nullable=False)

    role = Column(String, default="Visiteur", index=True)
    approved = Column(Boolean, default=False, index=True)

    subscription_expiry = Column(DateTime, nullable=True)

    created_at = Column(DateTime, server_default=func.now())

    # Relations
    properties = relationship(
        "Property",
        back_populates="owner",
        cascade="all, delete-orphan"
    )

    payments = relationship(
        "Payment",
        back_populates="user",
        cascade="all, delete-orphan"
    )


# ==========================
# PROPERTY MODEL
# ==========================
class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)

    titre = Column(String, nullable=False, index=True)
    description = Column(String, nullable=False)

    prix = Column(Integer, nullable=False, index=True)
    ville = Column(String, nullable=False, index=True)

    owner_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    created_at = Column(DateTime, server_default=func.now())

    owner = relationship("User", back_populates="properties")


# ==========================
# PAYMENT MODEL
# ==========================
class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    amount = Column(Integer, nullable=False)

    transaction_id = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    status = Column(String, default="pending", index=True)

    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="payments")