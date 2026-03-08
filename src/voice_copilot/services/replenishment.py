"""
Simplified replenishment service for MVP.
"""

from datetime import date, timedelta
from typing import List, Optional
from dataclasses import dataclass

from ..logging_config import get_logger
from ..exceptions import ReplenishmentException

logger = get_logger(__name__)


@dataclass
class OrderItem:
    """Replenishment order item."""
    sku: str
    sku_name: str
    suggested_quantity: float
    unit_cost: float
    total_cost: float
    urgency_level: str
    predicted_stockout_date: date
    current_stock: float


@dataclass
class ReplenishmentSuggestion:
    """Complete replenishment suggestion."""
    store_id: str
    generated_date: date
    total_estimated_cost: float
    order_items: List[OrderItem]
    priority_level: str


class ReplenishmentAgent:
    """Simplified replenishment suggestion service."""
    
    def suggest_replenishment(
        self,
        store_id: str,
        budget_limit: Optional[float] = None
    ) -> ReplenishmentSuggestion:
        """
        Generate replenishment suggestions.
        
        Args:
            store_id: Store identifier
            budget_limit: Optional budget constraint
            
        Returns:
            Replenishment suggestion with order items
        """
        try:
            # TODO: Replace with actual calculations using EOQ formula
            # For MVP, return mock data
            
            # Mock order items
            mock_items = [
                ("SKU-001", "Basmati Rice 5kg", 100, 250.0, 2),
                ("SKU-002", "Cooking Oil 1L", 80, 180.0, 4),
                ("SKU-007", "Lentils 1kg", 150, 120.0, 6),
            ]
            
            order_items = []
            total_cost = 0.0
            
            for sku, name, qty, unit_cost, days_until_stockout in mock_items:
                item_cost = qty * unit_cost
                
                # Check budget constraint
                if budget_limit and (total_cost + item_cost) > budget_limit:
                    continue
                
                # Determine urgency
                if days_until_stockout <= 3:
                    urgency = "HIGH"
                elif days_until_stockout <= 7:
                    urgency = "MEDIUM"
                else:
                    urgency = "LOW"
                
                stockout_date = date.today() + timedelta(days=days_until_stockout)
                
                order_items.append(OrderItem(
                    sku=sku,
                    sku_name=name,
                    suggested_quantity=qty,
                    unit_cost=unit_cost,
                    total_cost=item_cost,
                    urgency_level=urgency,
                    predicted_stockout_date=stockout_date,
                    current_stock=50.0  # Mock current stock
                ))
                
                total_cost += item_cost
            
            # Sort by stockout date (earliest first)
            order_items.sort(key=lambda x: x.predicted_stockout_date)
            
            # Determine overall priority
            if any(item.urgency_level == "HIGH" for item in order_items):
                priority = "URGENT"
            elif any(item.urgency_level == "MEDIUM" for item in order_items):
                priority = "NORMAL"
            else:
                priority = "LOW"
            
            suggestion = ReplenishmentSuggestion(
                store_id=store_id,
                generated_date=date.today(),
                total_estimated_cost=total_cost,
                order_items=order_items,
                priority_level=priority
            )
            
            logger.info(
                "replenishment_suggestion_complete",
                store_id=store_id,
                items_count=len(order_items),
                total_cost=total_cost
            )
            
            return suggestion
            
        except Exception as e:
            logger.error("replenishment_suggestion_error", error=str(e))
            raise ReplenishmentException(f"Failed to generate replenishment suggestion: {str(e)}")
