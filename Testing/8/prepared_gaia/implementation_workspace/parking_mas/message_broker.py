import asyncio
from typing import Dict, List, Callable
from .agent import Message


class MessageBroker:
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
        self.message_queue = asyncio.Queue()
        self.running = False

    def subscribe(self, topic: str, callback: Callable):
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(callback)

    def publish(self, message: Message):
        # In a real implementation, we would use a proper broker
        # For now, we'll simulate it with a queue
        asyncio.create_task(self._handle_message(message))

    async def _handle_message(self, message: Message):
        # Send to all subscribers for the receiver
        if message.receiver in self.subscribers:
            for callback in self.subscribers[message.receiver]:
                await callback(message)

    async def start(self):
        self.running = True
        asyncio.create_task(self._process_queue())

    async def stop(self):
        self.running = False

    async def _process_queue(self):
        while self.running:
            try:
                message = await asyncio.wait_for(self.message_queue.get(), timeout=1.0)
                self.publish(message)
                self.message_queue.task_done()
            except asyncio.TimeoutError:
                continue
