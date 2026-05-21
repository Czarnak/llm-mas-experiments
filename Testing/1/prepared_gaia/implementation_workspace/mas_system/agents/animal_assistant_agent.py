from agents.base_agent import BaseAgent
from typing import Dict, Any
import asyncio
import random


class AnimalAssistantAgent(BaseAgent):
    def __init__(self, agent_id: str):
        super().__init__(agent_id)
        self.animal_state = {
            "feed_state": "hungry",  # hungry, fed
            "walk_state": "needsWalk",  # needsWalk, walked
            "health_state": "healthy",  # healthy, sick
            "adoption_state": "available"  # available, adopted
        }
        self.feed_history = []
        self.walk_history = []
        self.health_history = []
        
    async def start(self):
        self.is_running = True
        print(f"Animal Assistant agent {self.agent_id} started with state {self.animal_state}")
        
        # Simulate periodic animal state checks and requests
        while self.is_running:
            await self.check_animal_state()
            await asyncio.sleep(6)  # Check animal state every 6 seconds
            
    async def handle_message(self, message: Dict[str, Any]):
        message_type = message.get("type")
        
        if message_type == "ConfirmFeedTask":
            await self.handle_confirm_feed_task(message)
        elif message_type == "ConfirmWalkTask":
            await self.handle_confirm_walk_task(message)
        elif message_type == "ConfirmHealthRequestTask":
            await self.handle_confirm_health_request_task(message)
        elif message_type == "ConfirmInitialCheckupTask":
            await self.handle_confirm_initial_checkup_task(message)
        elif message_type == "ConfirmAdoptionApplicationTask":
            await self.handle_confirm_adoption_application_task(message)
        else:
            print(f"Unknown message type: {message_type}")
            
    async def process_task(self, task_data: Dict[str, Any]):
        # Process a task that was assigned to this agent
        pass
        
    async def check_animal_state(self):
        # Simulate animal state changes and send requests when needed
        
        # Check if animal needs feeding
        if self.animal_state["feed_state"] == "hungry":
            feed_request = {
                "type": "newFeedRequest",
                "animalId": self.agent_id,
                "animalFeedState": self.animal_state["feed_state"]
            }
            
            print(f"Animal {self.agent_id}: Requesting feeding (state: {self.animal_state['feed_state']})")
            # In a real system, we would send this to coordinator
            # await self.send_message("coordinator", feed_request)
        
        # Check if animal needs walking
        if self.animal_state["walk_state"] == "needsWalk":
            walk_request = {
                "type": "newWalkRequest",
                "animalId": self.agent_id,
                "animalWalkState": self.animal_state["walk_state"]
            }
            
            print(f"Animal {self.agent_id}: Requesting walk (state: {self.animal_state['walk_state']})")
            # In a real system, we would send this to coordinator
            # await self.send_message("coordinator", walk_request)
        
        # Check if animal needs health attention
        if self.animal_state["health_state"] == "sick":
            health_request = {
                "type": "newHealthRequest",
                "animalId": self.agent_id,
                "animalHealthState": self.animal_state["health_state"]
            }
            
            print(f"Animal {self.agent_id}: Requesting health attention (state: {self.animal_state['health_state']})")
            # In a real system, we would send this to coordinator
            # await self.send_message("coordinator", health_request)
        
        # Randomly change animal states
        if random.random() < 0.1:  # 10% chance to change state
            states = ["hungry", "fed"]
            self.animal_state["feed_state"] = random.choice(states)
            
        if random.random() < 0.1:  # 10% chance to change state
            states = ["needsWalk", "walked"]
            self.animal_state["walk_state"] = random.choice(states)
            
        if random.random() < 0.05:  # 5% chance to change state
            states = ["healthy", "sick"]
            self.animal_state["health_state"] = random.choice(states)
            
    async def handle_confirm_feed_task(self, message: Dict[str, Any]):
        task_id = message.get("taskId")
        animal_id = message.get("animalId")
        
        # Update animal state
        self.animal_state["feed_state"] = "fed"
        
        # Add to feed history
        self.feed_history.append({
            "task_id": task_id,
            "animal_id": animal_id,
            "timestamp": "2023-01-01T00:00:00Z"
        })
        
        print(f"Animal {self.agent_id}: Feed task {task_id} confirmed, now fed")
        
    async def handle_confirm_walk_task(self, message: Dict[str, Any]):
        task_id = message.get("taskId")
        animal_id = message.get("animalId")
        
        # Update animal state
        self.animal_state["walk_state"] = "walked"
        
        # Add to walk history
        self.walk_history.append({
            "task_id": task_id,
            "animal_id": animal_id,
            "timestamp": "2023-01-01T00:00:00Z"
        })
        
        print(f"Animal {self.agent_id}: Walk task {task_id} confirmed, now walked")
        
    async def handle_confirm_health_request_task(self, message: Dict[str, Any]):
        task_id = message.get("taskId")
        animal_id = message.get("animalId")
        
        # Update animal state
        self.animal_state["health_state"] = "healthy"
        
        # Add to health history
        self.health_history.append({
            "task_id": task_id,
            "animal_id": animal_id,
            "timestamp": "2023-01-01T00:00:00Z"
        })
        
        print(f"Animal {self.agent_id}: Health task {task_id} confirmed, now healthy")
        
    async def handle_confirm_initial_checkup_task(self, message: Dict[str, Any]):
        task_id = message.get("taskId")
        animal_id = message.get("animalId")
        
        # Update animal state
        self.animal_state["health_state"] = "healthy"
        
        print(f"Animal {self.agent_id}: Initial checkup task {task_id} confirmed, now healthy")
        
    async def handle_confirm_adoption_application_task(self, message: Dict[str, Any]):
        task_id = message.get("taskId")
        animal_id = message.get("animalId")
        
        # Update animal state
        self.animal_state["adoption_state"] = "adopted"
        
        print(f"Animal {self.agent_id}: Adoption task {task_id} confirmed, now adopted")