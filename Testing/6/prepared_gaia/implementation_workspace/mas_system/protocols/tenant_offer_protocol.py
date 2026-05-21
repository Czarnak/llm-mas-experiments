from .base_protocol import BaseProtocol
from typing import Dict, Any, Optional


class TenantOfferProtocol(BaseProtocol):
    """
    Protocol for tenant offers
    """
    
    def __init__(self):
        super().__init__("TenantOffer")
        
    def validate_message(self, message: Dict[str, Any]) -> bool:
        required_fields = ['tenant_id', 'premise_id', 'bid_price', 'location', 'business_type']
        return all(field in message for field in required_fields)
    
    def process_message(self, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        # Process the tenant offer
        if not self.validate_message(message):
            return None
        
        # In a real implementation, this would process the offer
        # For now, we'll just return the same message with a status
        return {
            'status': 'processed',
            'message': message,
            'protocol': self.name
        }
    
    def create_offer_message(self, tenant_id: str, premise_id: str, bid_price: float, location: str, business_type: str) -> Dict[str, Any]:
        return {
            'tenant_id': tenant_id,
            'premise_id': premise_id,
            'bid_price': bid_price,
            'location': location,
            'business_type': business_type,
            'protocol': self.name
        }