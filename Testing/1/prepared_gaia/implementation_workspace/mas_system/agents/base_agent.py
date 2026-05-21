from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import asyncio


class BaseAgent(ABC):
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.state = {}
        self.is_running = False
        
    @abstractmethod
    async def start(self):
        pass
        
    @abstractmethod
    async def handle_message(self, message: Dict[str, Any]):
        pass
        
    @abstractmethod
    async def process_task(self, task_data: Dict[str, Any]):
        pass
        
    def get_state(self) -> Dict[str, Any]:
        return self.state
        
    def update_state(self, key: str, value: Any):
        self.state[key] = value
        
    async def send_message(self, recipient_id: str, message: Dict[str, Any]):
        # This will be implemented by the communication layer
        pass
        
    async def broadcast_message(self, message: Dict[str, Any]):
        # This will be implemented by the communication layer
        pass