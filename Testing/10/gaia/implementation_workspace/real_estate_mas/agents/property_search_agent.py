from langchain_core.tools import tool
from typing import Dict, Any
from models.property import RealEstateProperty
from models.property_report import PropertyReport
from datetime import datetime
import uuid


class PropertySearchAgent:
    """
    Agent responsible for searching properties by address and returning RealEstateProperty entities.
    """
    
    def __init__(self):
        self.name = "PropertySearchAgent"
        
    @tool
    def search_property_by_address(self, address: str) -> RealEstateProperty:
        """
        Search for a property by its address.
        
        Args:
            address (str): The full address of the property to search for
            
        Returns:
            RealEstateProperty: The found property with all its details
        """
        # In a real implementation, this would query a database or external API
        # For this simulation, we'll create a mock property
        
        if not address or len(address.strip()) < 5:
            raise ValueError("Address must be at least 5 characters long")
            
        # Generate a unique ID for the property
        property_id = str(uuid.uuid4())
        
        # Mock property data - in a real system this would come from a database/API
        mock_property_data = {
            "id": property_id,
            "address": address,
            "city": "Warsaw",
            "postal_code": "00-001",
            "latitude": 52.2297,
            "longitude": 21.0122,
            "property_type": "apartment",
            "price": 1200000.0,
            "bedrooms": 3,
            "bathrooms": 2,
            "area": 85.0,
            "year_built": 2010,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        return RealEstateProperty(**mock_property_data)
    
    def get_protocol_name(self) -> str:
        return "SearchPropertyByAddress"
    
    def get_protocol_description(self) -> str:
        return "Searches for a property by its address and returns a RealEstateProperty entity"
    
    def get_required_inputs(self) -> list:
        return ["address"]
    
    def get_outputs(self) -> list:
        return ["RealEstateProperty"]