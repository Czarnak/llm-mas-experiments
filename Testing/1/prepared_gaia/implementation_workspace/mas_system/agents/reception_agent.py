from agents.base_agent import BaseAgent
from typing import Dict, Any
import asyncio


class ReceptionAgent(BaseAgent):
    def __init__(self, agent_id: str):
        super().__init__(agent_id)
        self.animals = {}
        
    async def start(self):
        self.is_running = True
        print(f"Reception agent {self.agent_id} started")
        
        # Simulate periodic animal registration
        while self.is_running:
            await self.register_new_animal()
            await asyncio.sleep(5)  # Register new animal every 5 seconds
            
    async def handle_message(self, message: Dict[str, Any]):
        print(f"Reception agent {self.agent_id} received message: {message}")
        
    async def process_task(self, task_data: Dict[str, Any]):
        # Process a task that was assigned to this agent
        pass
        
    async def register_new_animal(self):
        # Simulate registering a new animal
        animal_id = f"animal_{len(self.animals) + 1}"
        animal_data = {
            "id": animal_id,
            "name": f"Animal_{len(self.animals) + 1}",
            "species": "dog" if len(self.animals) % 2 == 0 else "cat",
            "status": "new",
            "health": "healthy",
            "adoption_status": "available"
        }
        self.animals[animal_id] = animal_data
        
        # Send registration message to coordinator
        registration_message = {
            "type": "newAnimalRegistration",
            "animalId": animal_id,
            "animalData": animal_data
        }
        
        print(f"Reception: Registered new animal {animal_id}")
        # In a real system, we would send this to coordinator
        # await self.send_message("coordinator", registration_message)
