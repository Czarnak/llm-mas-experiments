from agents.base_agent import BaseAgent
from typing import Dict, Any
import asyncio


class AdoptionAgent(BaseAgent):
    def __init__(self, agent_id: str):
        super().__init__(agent_id)
        self.adoption_applications = {}
        self.adoption_process = {}
        
    async def start(self):
        self.is_running = True
        print(f"Adoption agent {self.agent_id} started")
        
        # Simulate processing adoption applications
        while self.is_running:
            await self.process_adoption_applications()
            await asyncio.sleep(3)  # Check for new applications every 3 seconds
            
    async def handle_message(self, message: Dict[str, Any]):
        message_type = message.get("type")
        
        if message_type == "newAdoptionApplication":
            await self.handle_new_adoption_application(message)
        elif message_type == "ConfirmAdoptionApplicationTask":
            await self.handle_confirm_adoption_application(message)
        else:
            print(f"Unknown message type: {message_type}")
        
    async def process_task(self, task_data: Dict[str, Any]):
        # Process a task that was assigned to this agent
        pass
        
    async def handle_new_adoption_application(self, message: Dict[str, Any]):
        application_id = f"app_{len(self.adoption_applications) + 1}"
        animal_id = message.get("animalId")
        applicant_id = message.get("applicantId")
        
        application_data = {
            "id": application_id,
            "animal_id": animal_id,
            "applicant_id": applicant_id,
            "status": "pending",
            "date": "2023-01-01"
        }
        
        self.adoption_applications[application_id] = application_data
        
        # Send confirmation to coordinator
        confirmation_message = {
            "type": "ConfirmAdoptionApplicationTask",
            "taskId": application_id,
            "animalId": animal_id,
            "status": "inProgress"
        }
        
        print(f"Adoption: New application {application_id} for animal {animal_id} received")
        # In a real system, we would send this to coordinator
        # await self.send_message("coordinator", confirmation_message)
        
    async def handle_confirm_adoption_application(self, message: Dict[str, Any]):
        task_id = message.get("taskId")
        animal_id = message.get("animalId")
        
        # Update adoption status
        self.adoption_process[animal_id] = "adopted"
        
        print(f"Adoption: Application {task_id} confirmed for animal {animal_id}")
        
    async def process_adoption_applications(self):
        # Simulate processing applications
        if self.adoption_applications:
            # In a real system, this would actually process applications
            pass