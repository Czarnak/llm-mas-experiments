from agents.base_agent import BaseAgent
from typing import Dict, Any, List
import asyncio


class WorkerAgent(BaseAgent):
    def __init__(self, agent_id: str):
        super().__init__(agent_id)
        self.role = "caretaker"  # Default role
        self.availability = {
            "status": "available",
            "role": "caretaker",
            "shift": "morning"
        }
        self.tasks = []
        
    async def start(self):
        self.is_running = True
        print(f"Worker agent {self.agent_id} started with role {self.role}")
        
        # Simulate periodic availability updates
        while self.is_running:
            await self.update_availability()
            await asyncio.sleep(10)  # Update availability every 10 seconds
            
    async def handle_message(self, message: Dict[str, Any]):
        message_type = message.get("type")
        
        if message_type == "AssignFeedTask":
            await self.handle_assign_feed_task(message)
        elif message_type == "AssignWalkTask":
            await self.handle_assign_walk_task(message)
        elif message_type == "AssignCleanTask":
            await self.handle_assign_clean_task(message)
        elif message_type == "AssignVaccinationTask":
            await self.handle_assign_vaccination_task(message)
        elif message_type == "AssignInitialCheckupTask":
            await self.handle_assign_initial_checkup_task(message)
        elif message_type == "HealthRequestTask":
            await self.handle_health_request_task(message)
        elif message_type == "UpdateWorkerAvailabilityTask":
            await self.handle_update_availability_task(message)
        elif message_type == "ConfirmFeedTask":
            await self.handle_confirm_feed_task(message)
        elif message_type == "ConfirmWalkTask":
            await self.handle_confirm_walk_task(message)
        elif message_type == "ConfirmCleanTask":
            await self.handle_confirm_clean_task(message)
        elif message_type == "ConfirmVaccinationTask":
            await self.handle_confirm_vaccination_task(message)
        elif message_type == "ConfirmInitialCheckupTask":
            await self.handle_confirm_initial_checkup_task(message)
        elif message_type == "ConfirmHealthRequestTask":
            await self.handle_confirm_health_request_task(message)
        elif message_type == "ConfirmUpdateWorkerAvailabilityTask":
            await self.handle_confirm_update_availability_task(message)
        else:
            print(f"Unknown message type: {message_type}")
            
    async def process_task(self, task_data: Dict[str, Any]):
        # Process a task that was assigned to this agent
        pass
        
    async def update_availability(self):
        # Simulate changing availability status
        statuses = ["available", "unavailable", "on_break"]
        self.availability["status"] = statuses[len(self.tasks) % len(statuses)]
        
        # Send availability update to coordinator
        availability_message = {
            "type": "newWorkerAvailability",
            "workerId": self.agent_id,
            "availability": self.availability
        }
        
        print(f"Worker {self.agent_id}: Updated availability to {self.availability['status']}")
        # In a real system, we would send this to coordinator
        # await self.send_message("coordinator", availability_message)
        
    async def handle_assign_feed_task(self, message: Dict[str, Any]):
        task_id = message.get("taskId")
        animal_id = message.get("animalId")
        
        self.tasks.append({
            "task_id": task_id,
            "type": "feed",
            "animal_id": animal_id,
            "status": "inProgress"
        })
        
        print(f"Worker {self.agent_id}: Assigned feeding task {task_id} for animal {animal_id}")
        
    async def handle_assign_walk_task(self, message: Dict[str, Any]):
        task_id = message.get("taskId")
        animal_id = message.get("animalId")
        
        self.tasks.append({
            "task_id": task_id,
            "type": "walk",
            "animal_id": animal_id,
            "status": "inProgress"
        })
        
        print(f"Worker {self.agent_id}: Assigned walking task {task_id} for animal {animal_id}")
        
    async def handle_assign_clean_task(self, message: Dict[str, Any]):
        task_id = message.get("taskId")
        room_id = message.get("roomId")
        
        self.tasks.append({
            "task_id": task_id,
            "type": "clean",
            "room_id": room_id,
            "status": "inProgress"
        })
        
        print(f"Worker {self.agent_id}: Assigned cleaning task {task_id} for room {room_id}")
        
    async def handle_assign_vaccination_task(self, message: Dict[str, Any]):
        task_id = message.get("taskId")
        animal_id = message.get("animalId")
        
        self.tasks.append({
            "task_id": task_id,
            "type": "vaccination",
            "animal_id": animal_id,
            "status": "inProgress"
        })
        
        print(f"Worker {self.agent_id}: Assigned vaccination task {task_id} for animal {animal_id}")
        
    async def handle_assign_initial_checkup_task(self, message: Dict[str, Any]):
        task_id = message.get("taskId")
        animal_id = message.get("animalId")
        
        self.tasks.append({
            "task_id": task_id,
            "type": "initial_checkup",
            "animal_id": animal_id,
            "status": "inProgress"
        })
        
        print(f"Worker {self.agent_id}: Assigned initial checkup task {task_id} for animal {animal_id}")
        
    async def handle_health_request_task(self, message: Dict[str, Any]):
        task_id = message.get("taskId")
        animal_id = message.get("animalId")
        
        self.tasks.append({
            "task_id": task_id,
            "type": "health",
            "animal_id": animal_id,
            "status": "inProgress"
        })
        
        print(f"Worker {self.agent_id}: Assigned health task {task_id} for animal {animal_id}")
        
    async def handle_update_availability_task(self, message: Dict[str, Any]):
        # This is just for handling the message, actual update is done in update_availability
        print(f"Worker {self.agent_id}: Received availability update request")
        
    async def handle_confirm_feed_task(self, message: Dict[str, Any]):
        task_id = message.get("taskId")
        animal_id = message.get("animalId")
        
        # Update task status
        for task in self.tasks:
            if task["task_id"] == task_id:
                task["status"] = "done"
                break
        
        print(f"Worker {self.agent_id}: Confirmed feeding task {task_id} for animal {animal_id}")
        
    async def handle_confirm_walk_task(self, message: Dict[str, Any]):
        task_id = message.get("taskId")
        animal_id = message.get("animalId")
        
        # Update task status
        for task in self.tasks:
            if task["task_id"] == task_id:
                task["status"] = "done"
                break
        
        print(f"Worker {self.agent_id}: Confirmed walking task {task_id} for animal {animal_id}")
        
    async def handle_confirm_clean_task(self, message: Dict[str, Any]):
        task_id = message.get("taskId")
        room_id = message.get("roomId")
        
        # Update task status
        for task in self.tasks:
            if task["task_id"] == task_id:
                task["status"] = "done"
                break
        
        print(f"Worker {self.agent_id}: Confirmed cleaning task {task_id} for room {room_id}")
        
    async def handle_confirm_vaccination_task(self, message: Dict[str, Any]):
        task_id = message.get("taskId")
        
        # Update task status
        for task in self.tasks:
            if task["task_id"] == task_id:
                task["status"] = "done"
                break
        
        print(f"Worker {self.agent_id}: Confirmed vaccination task {task_id}")
        
    async def handle_confirm_initial_checkup_task(self, message: Dict[str, Any]):
        task_id = message.get("taskId")
        animal_id = message.get("animalId")
        
        # Update task status
        for task in self.tasks:
            if task["task_id"] == task_id:
                task["status"] = "done"
                break
        
        print(f"Worker {self.agent_id}: Confirmed initial checkup task {task_id} for animal {animal_id}")
        
    async def handle_confirm_health_request_task(self, message: Dict[str, Any]):
        task_id = message.get("taskId")
        animal_id = message.get("animalId")
        
        # Update task status
        for task in self.tasks:
            if task["task_id"] == task_id:
                task["status"] = "done"
                break
        
        print(f"Worker {self.agent_id}: Confirmed health task {task_id} for animal {animal_id}")
        
    async def handle_confirm_update_availability_task(self, message: Dict[str, Any]):
        # Just acknowledge the update
        print(f"Worker {self.agent_id}: Confirmed availability update")