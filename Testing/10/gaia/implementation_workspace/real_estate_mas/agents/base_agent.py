from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseAgent(ABC):
    """
    Base class for all agents in the multi-agent system.
    """
    
    def __init__(self, name: str):
        self.name = name
        
    @abstractmethod
    def get_protocol_name(self) -> str:
        pass
        
    @abstractmethod
    def get_protocol_description(self) -> str:
        pass
        
    @abstractmethod
    def get_required_inputs(self) -> List[str]:
        pass
        
    @abstractmethod
    def get_outputs(self) -> List[str]:
        pass
        
    def __str__(self):
        return f"{self.name}"