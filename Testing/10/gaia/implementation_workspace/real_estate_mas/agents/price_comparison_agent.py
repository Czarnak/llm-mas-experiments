from langchain_core.tools import tool
from typing import Dict, Any
from models.property_comparison import PropertyComparison
from models.property import RealEstateProperty
from datetime import datetime
import uuid


class PriceComparisonAgent:
    """
    Agent responsible for comparing property prices with similar properties.
    """
    
    def __init__(self):
        self.name = "PriceComparisonAgent"
        
    @tool
    def compare_property_prices(self, property_id: str) -> PropertyComparison:
        """
        Compare the given property with similar properties in the area.
        
        Args:
            property_id (str): The ID of the property to compare
            
        Returns:
            PropertyComparison: Comparison data with similar properties
        """
        # In a real implementation, this would query property listing APIs or databases
        # For this simulation, we'll create mock comparison data
        
        if not property_id:
            raise ValueError("Property ID is required")
            
        # Generate a unique ID for the comparison
        comparison_id = str(uuid.uuid4())
        
        # Mock comparison data - in a real system this would come from property listings
        mock_comparison_data = {
            "id": comparison_id,
            "property_id": property_id,
            "similar_properties": [
                {
                    "id": str(uuid.uuid4()),
                    "address": "123 Main Street, Warsaw",
                    "price": 1150000.0,
                    "bedrooms": 3,
                    "bathrooms": 2,
                    "area": 80.0,
                    "price_per_sqm": 14375.0,
                    "distance": 0.5
                },
                {
                    "id": str(uuid.uuid4()),
                    "address": "456 Oak Avenue, Warsaw",
                    "price": 1300000.0,
                    "bedrooms": 3,
                    "bathrooms": 2,
                    "area": 90.0,
                    "price_per_sqm": 14444.4,
                    "distance": 1.2
                },
                {
                    "id": str(uuid.uuid4()),
                    "address": "789 Pine Road, Warsaw",
                    "price": 1250000.0,
                    "bedrooms": 3,
                    "bathrooms": 2,
                    "area": 85.0,
                    "price_per_sqm": 14705.9,
                    "distance": 0.8
                }
            ],
            "price_comparison": {
                "current_price": 1200000.0,
                "avg_comparable_price": 1233333.0,
                "price_difference": -2.7,
                "market_position": "slightly below average"
            },
            "property_features": {
                "bedrooms": 3,
                "bathrooms": 2,
                "area": 85.0,
                "year_built": 2010,
                "features": ["gym", "concierge", "parking"]
            },
            "market_data": {
                "area": "Warsaw Center",
                "market_trend": "slightly declining",
                "average_price_per_sqm": 14500.0,
                "time_on_market": 45
            },
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        return PropertyComparison(**mock_comparison_data)
    
    def get_protocol_name(self) -> str:
        return "ComparePropertyPrices"
    
    def get_protocol_description(self) -> str:
        return "Compares property price with similar properties in the area"
    
    def get_required_inputs(self) -> list:
        return ["property_id"]
    
    def get_outputs(self) -> list:
        return ["PropertyComparison"]