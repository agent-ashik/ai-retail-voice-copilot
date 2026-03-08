"""
User and store-related database models.
"""

from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey, Index, Enum as SQLEnum, Table, Column, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from .base import Base, TimestampMixin


class UserRole(str, enum.Enum):
    """User roles for access control."""
    STORE_MANAGER = "STORE_MANAGER"
    REGIONAL_MANAGER = "REGIONAL_MANAGER"
    ADMIN = "ADMIN"


# Association table for many-to-many relationship between users and stores
user_stores = Table(
    "user_stores",
    Base.metadata,
    Column("user_id", String(50), ForeignKey("users.user_id"), primary_key=True),
    Column("store_id", String(50), ForeignKey("stores.store_id"), primary_key=True),
)


class User(Base, TimestampMixin):
    """User accounts."""
    
    __tablename__ = "users"
    
    user_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str] = mapped_column(String(200), nullable=False, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(200), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole, name="user_role"),
        nullable=False,
        default=UserRole.STORE_MANAGER
    )
    preferred_language: Mapped[str] = mapped_column(String(10), default="en")
    primary_store_id: Mapped[Optional[str]] = mapped_column(
        String(50),
        ForeignKey("stores.store_id")
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Relationships
    assigned_stores = relationship("Store", secondary=user_stores, back_populates="users")
    primary_store = relationship("Store", foreign_keys=[primary_store_id])
    
    __table_args__ = (
        Index("idx_user_email", "email"),
        Index("idx_user_role", "role"),
    )


class Store(Base, TimestampMixin):
    """Store locations."""
    
    __tablename__ = "stores"
    
    store_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    address: Mapped[str] = mapped_column(String(500), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    state: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    country: Mapped[str] = mapped_column(String(100), nullable=False, default="India")
    timezone: Mapped[str] = mapped_column(String(50), default="Asia/Kolkata")
    operating_hours_open: Mapped[str] = mapped_column(String(10), default="06:00")
    operating_hours_close: Mapped[str] = mapped_column(String(10), default="23:00")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Relationships
    users = relationship("User", secondary=user_stores, back_populates="assigned_stores")
    inventory_records = relationship("InventoryRecord", back_populates="store")
    sales_transactions = relationship("SalesTransaction", back_populates="store")
    
    __table_args__ = (
        Index("idx_store_city", "city"),
        Index("idx_store_state", "state"),
        Index("idx_store_active", "is_active"),
    )
