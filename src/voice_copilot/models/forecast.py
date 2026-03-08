"""
Forecasting-related database models.
"""

from datetime import datetime, date
from typing import Optional
from sqlalchemy import String, Integer, Float, DateTime, Date, ForeignKey, Index, Enum as SQLEnum, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from .base import Base, TimestampMixin


class UrgencyLevel(str, enum.Enum):
    """Urgency levels for predictions."""
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class ForecastRecord(Base, TimestampMixin):
    """Demand forecast records."""
    
    __tablename__ = "forecast_records"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sku: Mapped[str] = mapped_column(String(50), ForeignKey("sku_master.sku"), nullable=False)
    store_id: Mapped[str] = mapped_column(String(50), ForeignKey("stores.store_id"), nullable=False)
    forecast_date: Mapped[date] = mapped_column(Date, nullable=False)
    predicted_demand: Mapped[float] = mapped_column(Float, nullable=False)
    confidence_lower: Mapped[float] = mapped_column(Float, nullable=False)
    confidence_upper: Mapped[float] = mapped_column(Float, nullable=False)
    model_version: Mapped[str] = mapped_column(String(50), nullable=False)
    generated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    store = relationship("Store")
    
    __table_args__ = (
        Index("idx_forecast_store_sku_date", "store_id", "sku", "forecast_date"),
        Index("idx_forecast_date", "forecast_date"),
        Index("idx_forecast_sku", "sku"),
    )


class StockoutPredictionRecord(Base, TimestampMixin):
    """Stockout prediction records."""
    
    __tablename__ = "stockout_predictions"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sku: Mapped[str] = mapped_column(String(50), ForeignKey("sku_master.sku"), nullable=False)
    store_id: Mapped[str] = mapped_column(String(50), ForeignKey("stores.store_id"), nullable=False)
    predicted_stockout_date: Mapped[date] = mapped_column(Date, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    current_stock: Mapped[float] = mapped_column(Float, nullable=False)
    average_daily_sales: Mapped[float] = mapped_column(Float, nullable=False)
    urgency_level: Mapped[UrgencyLevel] = mapped_column(
        SQLEnum(UrgencyLevel, name="urgency_level"),
        nullable=False
    )
    generated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    store = relationship("Store")
    
    __table_args__ = (
        Index("idx_stockout_store_sku", "store_id", "sku"),
        Index("idx_stockout_date", "predicted_stockout_date"),
        Index("idx_stockout_urgency", "urgency_level"),
    )


class ForecastAccuracyMetric(Base, TimestampMixin):
    """Forecast accuracy tracking."""
    
    __tablename__ = "forecast_accuracy_metrics"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    store_id: Mapped[str] = mapped_column(String(50), ForeignKey("stores.store_id"), nullable=False)
    sku: Mapped[Optional[str]] = mapped_column(String(50), ForeignKey("sku_master.sku"))
    category: Mapped[Optional[str]] = mapped_column(String(100))
    period_start: Mapped[date] = mapped_column(Date, nullable=False)
    period_end: Mapped[date] = mapped_column(Date, nullable=False)
    mape: Mapped[float] = mapped_column(Float, nullable=False)  # Mean Absolute Percentage Error
    rmse: Mapped[float] = mapped_column(Float, nullable=False)  # Root Mean Square Error
    accuracy_percentage: Mapped[float] = mapped_column(Float, nullable=False)
    flagged_for_review: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Relationships
    store = relationship("Store")
    
    __table_args__ = (
        Index("idx_accuracy_store_period", "store_id", "period_start", "period_end"),
        Index("idx_accuracy_category", "category"),
        Index("idx_accuracy_flagged", "flagged_for_review"),
    )
