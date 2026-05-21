from .base_protocol import BaseProtocol
from typing import Dict, Any, Optional


class PremiseOfferProtocol(BaseProtocol):
    """
    Protocol for offering premises for rent
    """
    
    def __init__(self):
        super().__init__("PremiseOffer")
        
    def validate_message(self, message: Dict[str, Any]) -> bool:
        required_fields = ['premise_id', 'location', 'price', 'size', 'business_type']
        return all(field in message for field in required_fields)
    
    def process_message(self, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        # Process the premise offer
        if not self.validate_message(message):
            return None
        
        # In a real implementation, this would process the offer
        # For now, we'll just return the same message with a status
        return {
            'status': 'processed',
            'message': message,
            'protocol': self.name
        }
    
    def create_offer_message(self, premise_id: str, location: str, price: float, size: float, business_type: str) -> Dict[str, Any]:
        return {
            'premise_id': premise_id,
            'location': location,
            'price': price,
            'size': size,
            'business_type': business_type,
            'protocol': self.name
        }