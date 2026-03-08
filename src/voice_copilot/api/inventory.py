"""
Inventory-related API endpoints.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from pydantic import BaseModel

from ..services.forecasting import ForecastingService, StockoutPrediction
from ..services.inventory import InventoryAnalyzer, OverstockItem
from ..services.replenishment import ReplenishmentAgent, ReplenishmentSuggestion
from ..logging_config import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/v1", tags=["inventory"])


# Request/Response models
class StockoutRequest(BaseModel):
    store_id: str
    days_ahead: int = 7
    sku_filters: Optional[List[str]] = None


class OverstockRequest(BaseModel):
    store_id: str
    category_filters: Optional[List[str]] = None


class ReplenishmentRequest(BaseModel):
    store_id: str
    budget_limit: Optional[float] = None


@router.post("/query/stockout")
async def predict_stockouts(request: StockoutRequest):
    """
    Predict stockouts for a store.
    
    Returns list of SKUs predicted to stock out within the specified timeframe.
    """
    try:
        service = ForecastingService()
        predictions = service.predict_stockouts(
            store_id=request.store_id,
            days_ahead=request.days_ahead,
            sku_filters=request.sku_filters
        )
        
        return {
            "success": True,
            "store_id": request.store_id,
            "predictions_count": len(predictions),
            "predictions": [
                {
                    "sku": p.sku,
                    "sku_name": p.sku_name,
                    "current_stock": p.current_stock,
                    "predicted_stockout_date": p.predicted_stockout_date.isoformat(),
                    "confidence": p.confidence,
                    "urgency_level": p.urgency_level
                }
                for p in predictions
            ]
        }
    except Exception as e:
        logger.error("stockout_api_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/query/overstock")
async def detect_overstock(request: OverstockRequest):
    """
    Detect overstocked items for a store.
    
    Returns list of SKUs with excess inventory.
    """
    try:
        analyzer = InventoryAnalyzer()
        overstocked = analyzer.detect_overstock(
            store_id=request.store_id,
            category_filters=request.category_filters
        )
        
        return {
            "success": True,
            "store_id": request.store_id,
            "overstocked_count": len(overstocked),
            "overstocked_items": [
                {
                    "sku": item.sku,
                    "sku_name": item.sku_name,
                    "current_stock": item.current_stock,
                    "max_threshold": item.max_threshold,
                    "excess_quantity": item.excess_quantity,
                    "excess_percentage": round(item.excess_percentage, 2),
                    "days_of_supply": round(item.days_of_supply, 1)
                }
                for item in overstocked
            ]
        }
    except Exception as e:
        logger.error("overstock_api_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/query/replenishment")
async def suggest_replenishment(request: ReplenishmentRequest):
    """
    Generate replenishment order suggestions for a store.
    
    Returns optimized order suggestions with cost estimates.
    """
    try:
        agent = ReplenishmentAgent()
        suggestion = agent.suggest_replenishment(
            store_id=request.store_id,
            budget_limit=request.budget_limit
        )
        
        return {
            "success": True,
            "store_id": suggestion.store_id,
            "generated_date": suggestion.generated_date.isoformat(),
            "total_estimated_cost": suggestion.total_estimated_cost,
            "priority_level": suggestion.priority_level,
            "order_items_count": len(suggestion.order_items),
            "order_items": [
                {
                    "sku": item.sku,
                    "sku_name": item.sku_name,
                    "suggested_quantity": item.suggested_quantity,
                    "unit_cost": item.unit_cost,
                    "total_cost": item.total_cost,
                    "urgency_level": item.urgency_level,
                    "predicted_stockout_date": item.predicted_stockout_date.isoformat(),
                    "current_stock": item.current_stock
                }
                for item in suggestion.order_items
            ]
        }
    except Exception as e:
        logger.error("replenishment_api_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))
