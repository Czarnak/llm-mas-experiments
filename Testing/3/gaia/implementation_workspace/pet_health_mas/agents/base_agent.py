from abc import ABC, abstractmethod
from typing import Dict, Any, List
from pydantic import BaseModel


class Agent(BaseModel):
    name: str
    role: str
    
    class Config:
        arbitrary_types_allowed = True

    @abstractmethod
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_capabilities(self) -> List[str]:
        pass

    @abstractmethod
    def get_safety_conditions(self) -> List[str]:
        pass

    @abstractmethod
    def get_liveness_conditions(self) -> str:
        pass