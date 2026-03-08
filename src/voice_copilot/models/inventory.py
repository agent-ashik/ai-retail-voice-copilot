"""
Inventory-related database models.
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey, Index, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin


class SKUMaster(Base, TimestampMixin):
    """Master data for Stock Keeping Units (SKUs)."""
    
    __tablename__ = "sku_master"
    
    sku: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    subcategory: Mapped[Optional[str]] = mapped_column(String(100))
    brand: Mapped[Optional[str]] = mapped_column(String(100))
    unit_of_measure: Mapped[str] = mapped_column(String(20), default="units")
    perishable: Mapped[bool] = mapped_column(Boolean, default=False)
    shelf_life_days: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Relationships
    inventory_records = relationship("InventoryRecord", back_populates="sku_master")
    sales_transactions = relationship("SalesTransaction", back_populates="sku_master")
    
    __table_args__ = (
        Index("idx_sku_category", "category"),
        Index("idx_sku_brand", "brand"),
    )


class InventoryRecord(Base, TimestampMixin):
    """Current inventory levels for SKUs at stores."""
    
    __tablename__ = "inventory_records"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sku: Mapped[str] = mapped_column(String(50), ForeignKey("sku_master.sku"), nullable=False)
    store_id: Mapped[str] = mapped_column(String(50), ForeignKey("stores.store_id"), nullable=False)
    current_stock: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    min_threshold: Mapped[float] = mapped_column(Float, nullable=False)
    max_threshold: Mapped[float] = mapped_column(Float, nullable=False)
    reorder_point: Mapped[float] = mapped_column(Float, nullable=False)
    unit_cost: Mapped[float] = mapped_column(Float, nullable=False)
    location: Mapped[Optional[str]] = mapped_column(String(100))
    last_updated: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    sku_master = relationship("SKUMaster", back_populates="inventory_records")
    store = relationship("Store", back_populates="inventory_records")
    
    __table_args__ = (
        Index("idx_inventory_sku_store", "sku", "store_id", unique=True),
        Index("idx_inventory_store", "store_id"),
        Index("idx_inventory_sku", "sku"),
    )
