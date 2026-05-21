from .base_protocol import BaseProtocol
from typing import Dict, Any, Optional


class ServiceDemandProtocol(BaseProtocol):
    """
    Protocol for reporting service demands from citizens
    """
    
    def __init__(self):
        super().__init__("ServiceDemandRequest")
        
    def validate_message(self, message: Dict[str, Any]) -> bool:
        required_fields = ['citizen_id', 'service_type', 'location', 'priority']
        return all(field in message for field in required_fields)
    
    def process_message(self, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        # Process the service demand
        if not self.validate_message(message):
            return None
        
        # In a real implementation, this would process the demand
        # For now, we'll just return the same message with a status
        return {
            'status': 'processed',
            'message': message,
            'protocol': self.name
        }
    
    def create_demand_message(self, citizen_id: str, service_type: str, location: str, priority: str) -> Dict[str, Any]:
        return {
            'citizen_id': citizen_id,
            'service_type': service_type,
            'location': location,
            'priority': priority,
            'protocol': self.name
        }