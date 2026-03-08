"""
Simplified forecasting service for MVP.
"""

from datetime import datetime, date, timedelta
from typing import List, Optional
from dataclasses import dataclass

from ..logging_config import get_logger
from ..exceptions import ForecastingException, InsufficientDataException

logger = get_logger(__name__)


@dataclass
class StockoutPrediction:
    """Stockout prediction result."""
    sku: str
    sku_name: str
    current_stock: float
    predicted_stockout_date: date
    confidence: float
    urgency_level: str  # HIGH, MEDIUM, LOW


class ForecastingService:
    """Simplified forecasting service using basic calculations."""
    
    def predict_stockouts(
        self,
        store_id: str,
        days_ahead: int = 7,
        sku_filters: Optional[List[str]] = None
    ) -> List[StockoutPrediction]:
        """
        Predict stockouts using simple linear projection.
        
        Args:
            store_id: Store identifier
            days_ahead: Number of days to forecast
            sku_filters: Optional list of SKUs to filter
            
        Returns:
            List of stockout predictions
        """
        try:
            # TODO: Replace with actual database queries and Prophet/ARIMA models
            # For MVP, return mock data
            predictions = []
            
            # Mock data for demonstration
            mock_skus = [
                ("SKU-001", "Basmati Rice 5kg", 50, 10, 0.85),
                ("SKU-002", "Cooking Oil 1L", 30, 8, 0.90),
                ("SKU-003", "Sugar 1kg", 20, 5, 0.88),
            ]
            
            for sku, name, stock, daily_sales, confidence in mock_skus:
                if sku_filters and sku not in sku_filters:
                    continue
                
                # Calculate days until stockout
                days_until_stockout = stock / daily_sales if daily_sales > 0 else 999
                
                if days_until_stockout <= days_ahead:
                    stockout_date = date.today() + timedelta(days=int(days_until_stockout))
                    
                    # Determine urgency
                    if days_until_stockout <= 3:
                        urgency = "HIGH"
                    elif days_until_stockout <= 7:
                        urgency = "MEDIUM"
                    else:
                        urgency = "LOW"
                    
                    predictions.append(StockoutPrediction(
                        sku=sku,
                        sku_name=name,
                        current_stock=stock,
                        predicted_stockout_date=stockout_date,
                        confidence=confidence,
                        urgency_level=urgency
                    ))
            
            # Sort by stockout date (earliest first)
            predictions.sort(key=lambda x: x.predicted_stockout_date)
            
            logger.info(
                "stockout_prediction_complete",
                store_id=store_id,
                predictions_count=len(predictions)
            )
            
            return predictions
            
        except Exception as e:
            logger.error("stockout_prediction_error", error=str(e))
            raise ForecastingException(f"Failed to predict stockouts: {str(e)}")
