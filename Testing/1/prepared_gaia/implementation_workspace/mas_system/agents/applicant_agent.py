from agents.base_agent import BaseAgent
from typing import Dict, Any
import asyncio
import random


class ApplicantAgent(BaseAgent):
    def __init__(self, agent_id: str):
        super().__init__(agent_id)
        self.applications = []
        self.adoption_status = "available"  # available, interested, adopted
        
    async def start(self):
        self.is_running = True
        print(f"Applicant agent {self.agent_id} started")
        
        # Simulate periodic adoption application requests
        while self.is_running:
            await self.submit_adoption_application()
            await asyncio.sleep(12)  # Submit application every 12 seconds
            
    async def handle_message(self, message: Dict[str, Any]):
        message_type = message.get("type")
        
        if message_type == "ConfirmAdoptionApplicationTask":
            await self.handle_confirm_adoption_application(message)
        else:
            print(f"Unknown message type: {message_type}")
            
    async def process_task(self, task_data: Dict[str, Any]):
        # Process a task that was assigned to this agent
        pass
        
    async def submit_adoption_application(self):
        # Simulate submitting an adoption application
        # In a real system, this would be triggered by a user action
        
        # Randomly select an animal to apply for
        animal_id = f"animal_{random.randint(1, 5)}"
        
        # Check if animal is available for adoption
        if self.adoption_status == "available":  # In a real system, we'd check actual state
            application = {
                "type": "newAdoptionApplication",
                "animalId": animal_id,
                "applicantId": self.agent_id,
                "status": "pending"
            }
            
            self.applications.append(application)
            
            print(f"Applicant {self.agent_id}: Submitted adoption application for animal {animal_id}")
            # In a real system, we would send this to coordinator
            # await self.send_message("coordinator", application)
        
    async def handle_confirm_adoption_application(self, message: Dict[str, Any]):
        task_id = message.get("taskId")
        animal_id = message.get("animalId")
        
        # Update adoption status
        self.adoption_status = "adopted"
        
        print(f"Applicant {self.agent_id}: Adoption application {task_id} confirmed for animal {animal_id}")
        
        # Reset status for next application
        # This is a simplified version - in reality, the applicant would need to be reset
        # or a new applicant would be created
        self.adoption_status = "available"  # Reset for next adoption attempt
        
        # In a real system, this would be handled by the adoption process and coordinator