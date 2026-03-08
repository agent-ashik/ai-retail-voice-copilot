"""
Simplified inventory analysis service for MVP.
"""

from typing import List, Optional
from dataclasses import dataclass

from ..logging_config import get_logger
from ..exceptions import InventoryAnalysisException

logger = get_logger(__name__)


@dataclass
class OverstockItem:
    """Overstock detection result."""
    sku: str
    sku_name: str
    current_stock: float
    max_threshold: float
    excess_quantity: float
    excess_percentage: float
    days_of_supply: float


class InventoryAnalyzer:
    """Simplified inventory analysis service."""
    
    def __init__(self, overstock_threshold: float = 1.5):
        """
        Initialize inventory analyzer.
        
        Args:
            overstock_threshold: Multiplier for overstock detection (default 1.5 = 150%)
        """
        self.overstock_threshold = overstock_threshold
    
    def detect_overstock(
        self,
        store_id: str,
        category_filters: Optional[List[str]] = None
    ) -> List[OverstockItem]:
        """
        Detect overstocked items.
        
        Args:
            store_id: Store identifier
            category_filters: Optional list of categories to filter
            
        Returns:
            List of overstocked items
        """
        try:
            # TODO: Replace with actual database queries
            # For MVP, return mock data
            overstocked = []
            
            # Mock data for demonstration
            mock_items = [
                ("SKU-004", "Wheat Flour 10kg", 500, 200, 5),
                ("SKU-005", "Tea Bags 100ct", 800, 300, 8),
                ("SKU-006", "Coffee Powder 500g", 350, 150, 6),
            ]
            
            for sku, name, stock, max_thresh, daily_sales in mock_items:
                # Check if overstocked
                if stock > (max_thresh * self.overstock_threshold):
                    excess_qty = stock - max_thresh
                    excess_pct = ((stock - max_thresh) / max_thresh) * 100
                    days_supply = stock / daily_sales if daily_sales > 0 else 999
                    
                    overstocked.append(OverstockItem(
                        sku=sku,
                        sku_name=name,
                        current_stock=stock,
                        max_threshold=max_thresh,
                        excess_quantity=excess_qty,
                        excess_percentage=excess_pct,
                        days_of_supply=days_supply
                    ))
            
            # Sort by excess percentage (highest first)
            overstocked.sort(key=lambda x: x.excess_percentage, reverse=True)
            
            logger.info(
                "overstock_detection_complete",
                store_id=store_id,
                overstocked_count=len(overstocked)
            )
            
            return overstocked
            
        except Exception as e:
            logger.error("overstock_detection_error", error=str(e))
            raise InventoryAnalysisException(f"Failed to detect overstock: {str(e)}")
