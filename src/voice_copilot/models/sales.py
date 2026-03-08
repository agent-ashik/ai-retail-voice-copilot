"""
Sales-related database models.
"""

from datetime import datetime, date
from typing import Optional
from sqlalchemy import String, Integer, Float, DateTime, Date, ForeignKey, Index, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin


class SalesTransaction(Base, TimestampMixin):
    """Individual sales transactions."""
    
    __tablename__ = "sales_transactions"
    
    transaction_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    store_id: Mapped[str] = mapped_column(String(50), ForeignKey("stores.store_id"), nullable=False)
    sku: Mapped[str] = mapped_column(String(50), ForeignKey("sku_master.sku"), nullable=False)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    unit_price: Mapped[float] = mapped_column(Float, nullable=False)
    total_amount: Mapped[float] = mapped_column(Float, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    promotion_applied: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Relationships
    store = relationship("Store", back_populates="sales_transactions")
    sku_master = relationship("SKUMaster", back_populates="sales_transactions")
    
    __table_args__ = (
        Index("idx_sales_store_date", "store_id", "timestamp"),
        Index("idx_sales_sku_date", "sku", "timestamp"),
        Index("idx_sales_timestamp", "timestamp"),
    )


class DailySalesSummary(Base, TimestampMixin):
    """Aggregated daily sales data for performance."""
    
    __tablename__ = "daily_sales_summary"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    store_id: Mapped[str] = mapped_column(String(50), ForeignKey("stores.store_id"), nullable=False)
    sku: Mapped[str] = mapped_column(String(50), ForeignKey("sku_master.sku"), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    total_quantity_sold: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    total_revenue: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    transaction_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    
    # Relationships
    store = relationship("Store")
    
    __table_args__ = (
        Index("idx_daily_sales_store_sku_date", "store_id", "sku", "date", unique=True),
        Index("idx_daily_sales_date", "date"),
        Index("idx_daily_sales_sku", "sku"),
    )
