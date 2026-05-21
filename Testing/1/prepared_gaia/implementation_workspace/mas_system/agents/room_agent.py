from agents.base_agent import BaseAgent
from typing import Dict, Any
import asyncio
import random


class RoomAgent(BaseAgent):
    def __init__(self, agent_id: str):
        super().__init__(agent_id)
        self.room_state = "dirty"  # Default state
        self.cleaning_history = []
        
    async def start(self):
        self.is_running = True
        print(f"Room agent {self.agent_id} started with state {self.room_state}")
        
        # Simulate periodic room state changes and cleaning requests
        while self.is_running:
            await self.check_room_state()
            await asyncio.sleep(8)  # Check room state every 8 seconds
            
    async def handle_message(self, message: Dict[str, Any]):
        message_type = message.get("type")
        
        if message_type == "ConfirmCleanTask":
            await self.handle_confirm_clean_task(message)
        else:
            print(f"Unknown message type: {message_type}")
            
    async def process_task(self, task_data: Dict[str, Any]):
        # Process a task that was assigned to this agent
        pass
        
    async def check_room_state(self):
        # Simulate room state changes
        if self.room_state == "dirty":
            # Send cleaning request
            clean_request = {
                "type": "newCleanRequest",
                "roomId": self.agent_id,
                "roomState": self.room_state
            }
            
            print(f"Room {self.agent_id}: Requesting cleaning (state: {self.room_state})")
            # In a real system, we would send this to coordinator
            # await self.send_message("coordinator", clean_request)
        else:
            # Randomly change room state
            states = ["dirty", "clean", "clean"]  # More likely to be clean
            self.room_state = random.choice(states)
            
            if self.room_state == "dirty":
                print(f"Room {self.agent_id}: State changed to dirty")
                
    async def handle_confirm_clean_task(self, message: Dict[str, Any]):
        task_id = message.get("taskId")
        room_id = message.get("roomId")
        
        # Update room state
        self.room_state = "clean"
        
        # Add to cleaning history
        self.cleaning_history.append({
            "task_id": task_id,
            "room_id": room_id,
            "timestamp": "2023-01-01T00:00:00Z"
        })
        
        print(f"Room {self.agent_id}: Cleaning task {task_id} confirmed, now clean")