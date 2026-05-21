import asyncio
import json
from typing import Dict, Any, Optional
from pydantic import BaseModel


class Message(BaseModel):
    sender: str
    receiver: str
    protocol: str
    content: Dict[str, Any]
    message_id: str


class Agent:
    def __init__(self, agent_id: str, agent_type: str):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.message_queue = asyncio.Queue()
        self.running = False

    async def start(self):
        self.running = True
        asyncio.create_task(self._process_messages())

    async def stop(self):
        self.running = False

    async def _process_messages(self):
        while self.running:
            try:
                message = await asyncio.wait_for(self.message_queue.get(), timeout=1.0)
                await self.handle_message(message)
                self.message_queue.task_done()
            except asyncio.TimeoutError:
                continue

    async def handle_message(self, message: Message):
        raise NotImplementedError("Subclasses must implement handle_message")

    async def send_message(self, message: Message):
        # In a real implementation, this would go through a broker
        pass

    def get_role(self) -> str:
        return self.agent_type
