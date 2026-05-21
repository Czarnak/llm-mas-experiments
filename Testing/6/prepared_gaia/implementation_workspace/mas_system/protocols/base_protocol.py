from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseProtocol(ABC):
    """
    Base class for all protocols in the Multi-Agent System
    """
    
    def __init__(self, name: str):
        self.name = name
        
    @abstractmethod
    def validate_message(self, message: Dict[str, Any]) -> bool:
        """
        Validate if the message conforms to this protocol
        """
        pass
    
    @abstractmethod
    def process_message(self, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process the message according to this protocol
        """
        pass
    
    def get_protocol_info(self) -> Dict[str, Any]:
        """
        Get information about this protocol
        """
        return {
            'name': self.name,
            'type': self.__class__.__name__
        }