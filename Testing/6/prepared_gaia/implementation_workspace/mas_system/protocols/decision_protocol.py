from .base_protocol import BaseProtocol
from typing import Dict, Any, Optional


class DecisionProtocol(BaseProtocol):
    """
    Protocol for making decisions on offers
    """
    
    def __init__(self):
        super().__init__("DecideOffer")
        
    def validate_message(self, message: Dict[str, Any]) -> bool:
        required_fields = ['offer_id', 'decision', 'reason']
        return all(field in message for field in required_fields)
    
    def process_message(self, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        # Process the decision
        if not self.validate_message(message):
            return None
        
        # In a real implementation, this would process the decision
        # For now, we'll just return the same message with a status
        return {
            'status': 'processed',
            'message': message,
            'protocol': self.name
        }
    
    def create_decision_message(self, offer_id: str, decision: str, reason: str) -> Dict[str, Any]:
        return {
            'offer_id': offer_id,
            'decision': decision,
            'reason': reason,
            'protocol': self.name
        }