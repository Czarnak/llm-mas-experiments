from agents.base_agent import BaseAgent
from typing import Dict, Any, List
import asyncio
import random


class CoordinatorAgent(BaseAgent):
    def __init__(self, agent_id: str):
        super().__init__(agent_id)
        self.worker_availability = {}
        self.task_queue = []
        self.assigned_tasks = {}
        self.animal_states = {}
        self.room_states = {}
        self.adoption_states = {}
        
    async def start(self):
        self.is_running = True
        print(f"Coordinator agent {self.agent_id} started")
        
        # Simulate periodic task assignment
        while self.is_running:
            await self.assign_tasks()
            await asyncio.sleep(2)  # Check for new tasks every 2 seconds
            
    async def handle_message(self, message: Dict[str, Any]):
        message_type = message.get("type")
        
        if message_type == "newCleanRequest":
            await self.handle_clean_request(message)
        elif message_type == "newFeedRequest":
            await self.handle_feed_request(message)
        elif message_type == "newWalkRequest":
            await self.handle_walk_request(message)
        elif message_type == "newHealthRequest":
            await self.handle_health_request(message)
        elif message_type == "newAnimalRegistration":
            await self.handle_new_animal_registration(message)
        elif message_type == "newAdoptionApplication":
            await self.handle_adoption_application(message)
        elif message_type == "newWorkerAvailability":
            await self.handle_worker_availability_update(message)
        elif message_type == "ConfirmCleanTask":
            await self.handle_confirm_clean_task(message)
        elif message_type == "ConfirmFeedTask":
            await self.handle_confirm_feed_task(message)
        elif message_type == "ConfirmWalkTask":
            await self.handle_confirm_walk_task(message)
        elif message_type == "ConfirmVaccinationTask":
            await self.handle_confirm_vaccination_task(message)
        elif message_type == "ConfirmInitialCheckupTask":
            await self.handle_confirm_initial_checkup_task(message)
        elif message_type == "ConfirmHealthRequestTask":
            await self.handle_confirm_health_request_task(message)
        elif message_type == "ConfirmAdoptionApplicationTask":
            await self.handle_confirm_adoption_application_task(message)
        elif message_type == "ConfirmUpdateWorkerAvailabilityTask":
            await self.handle_confirm_update_worker_availability_task(message)
        else:
            print(f"Unknown message type: {message_type}")
            
    async def process_task(self, task_data: Dict[str, Any]):
        # Process a task that was assigned to this agent
        pass
        
    async def assign_tasks(self):
        # Assign tasks based on availability and needs
        pass
        
    async def handle_clean_request(self, message: Dict[str, Any]):
        room_id = message.get("roomId")
        # Check if task already assigned
        if not self.is_task_assigned("clean", room_id):
            # Find available cleaner
            available_worker = self.find_available_worker("cleaner")
            if available_worker:
                task_id = f"task_clean_{room_id}_{len(self.task_queue)}"
                self.task_queue.append({
                    "task_id": task_id,
                    "type": "clean",
                    "room_id": room_id,
                    "worker_id": available_worker
                })
                print(f"Coordinator: Assigned cleaning task {task_id} to {available_worker}")
                
    async def handle_feed_request(self, message: Dict[str, Any]):
        animal_id = message.get("animalId")
        # Check if task already assigned
        if not self.is_task_assigned("feed", animal_id):
            # Find available caretaker
            available_worker = self.find_available_worker("caretaker")
            if available_worker:
                task_id = f"task_feed_{animal_id}_{len(self.task_queue)}"
                self.task_queue.append({
                    "task_id": task_id,
                    "type": "feed",
                    "animal_id": animal_id,
                    "worker_id": available_worker
                })
                print(f"Coordinator: Assigned feeding task {task_id} to {available_worker}")
                
    async def handle_walk_request(self, message: Dict[str, Any]):
        animal_id = message.get("animalId")
        # Check if task already assigned
        if not self.is_task_assigned("walk", animal_id):
            # Find available caretaker
            available_worker = self.find_available_worker("caretaker")
            if available_worker:
                task_id = f"task_walk_{animal_id}_{len(self.task_queue)}"
                self.task_queue.append({
                    "task_id": task_id,
                    "type": "walk",
                    "animal_id": animal_id,
                    "worker_id": available_worker
                })
                print(f"Coordinator: Assigned walking task {task_id} to {available_worker}")
                
    async def handle_health_request(self, message: Dict[str, Any]):
        animal_id = message.get("animalId")
        # Check if task already assigned
        if not self.is_task_assigned("health", animal_id):
            # Find available veterinarian
            available_worker = self.find_available_worker("veterinarian")
            if available_worker:
                task_id = f"task_health_{animal_id}_{len(self.task_queue)}"
                self.task_queue.append({
                    "task_id": task_id,
                    "type": "health",
                    "animal_id": animal_id,
                    "worker_id": available_worker
                })
                print(f"Coordinator: Assigned health task {task_id} to {available_worker}")
                
    async def handle_new_animal_registration(self, message: Dict[str, Any]):
        animal_id = message.get("animalId")
        # Find available veterinarian
        available_worker = self.find_available_worker("veterinarian")
        if available_worker:
            task_id = f"task_checkup_{animal_id}_{len(self.task_queue)}"
            self.task_queue.append({
                "task_id": task_id,
                "type": "initial_checkup",
                "animal_id": animal_id,
                "worker_id": available_worker
            })
            print(f"Coordinator: Assigned initial checkup task {task_id} to {available_worker}")
            
    async def handle_adoption_application(self, message: Dict[str, Any]):
        animal_id = message.get("animalId")
        # Find available adoption agent
        task_id = f"task_adoption_{animal_id}_{len(self.task_queue)}"
        self.task_queue.append({
            "task_id": task_id,
            "type": "adoption",
            "animal_id": animal_id,
            "worker_id": "adoption"
        })
        print(f"Coordinator: Assigned adoption task {task_id} to adoption agent")
        
    async def handle_worker_availability_update(self, message: Dict[str, Any]):
        worker_id = message.get("workerId")
        availability = message.get("availability")
        self.worker_availability[worker_id] = availability
        print(f"Coordinator: Updated availability for worker {worker_id}")
        
    async def handle_confirm_clean_task(self, message: Dict[str, Any]):
        task_id = message.get("taskId")
        room_id = message.get("roomId")
        # Update room state
        self.room_states[room_id] = "clean"
        # Update task status
        self.update_task_status(task_id, "done")
        print(f"Coordinator: Clean task {task_id} confirmed and room {room_id} marked clean")
        
    async def handle_confirm_feed_task(self, message: Dict[str, Any]):
        task_id = message.get("taskId")
        animal_id = message.get("animalId")
        # Update animal state
        self.animal_states[animal_id] = "fed"
        # Update task status
        self.update_task_status(task_id, "done")
        print(f"Coordinator: Feed task {task_id} confirmed and animal {animal_id} marked fed")
        
    async def handle_confirm_walk_task(self, message: Dict[str, Any]):
        task_id = message.get("taskId")
        animal_id = message.get("animalId")
        # Update animal state
        self.animal_states[animal_id] = "walked"
        # Update task status
        self.update_task_status(task_id, "done")
        print(f"Coordinator: Walk task {task_id} confirmed and animal {animal_id} marked walked")
        
    async def handle_confirm_vaccination_task(self, message: Dict[str, Any]):
        task_id = message.get("taskId")
        # Update task status
        self.update_task_status(task_id, "done")
        print(f"Coordinator: Vaccination task {task_id} confirmed")
        
    async def handle_confirm_initial_checkup_task(self, message: Dict[str, Any]):
        task_id = message.get("taskId")
        animal_id = message.get("animalId")
        # Update animal health state
        self.animal_states[animal_id] = "healthy"
        # Update task status
        self.update_task_status(task_id, "done")
        print(f"Coordinator: Initial checkup task {task_id} confirmed and animal {animal_id} marked healthy")
        
    async def handle_confirm_health_request_task(self, message: Dict[str, Any]):
        task_id = message.get("taskId")
        animal_id = message.get("animalId")
        # Update animal health state
        self.animal_states[animal_id] = "healthy"
        # Update task status
        self.update_task_status(task_id, "done")
        print(f"Coordinator: Health request task {task_id} confirmed and animal {animal_id} marked healthy")
        
    async def handle_confirm_adoption_application_task(self, message: Dict[str, Any]):
        task_id = message.get("taskId")
        animal_id = message.get("animalId")
        # Update adoption state
        self.adoption_states[animal_id] = "adopted"
        # Update task status
        self.update_task_status(task_id, "done")
        print(f"Coordinator: Adoption task {task_id} confirmed and animal {animal_id} marked adopted")
        
    async def handle_confirm_update_worker_availability_task(self, message: Dict[str, Any]):
        # Just acknowledge the update
        print(f"Coordinator: Worker availability update confirmed")
        
    def find_available_worker(self, role: str) -> Optional[str]:
        # Simple logic to find an available worker of a specific role
        for worker_id, availability in self.worker_availability.items():
            if availability.get("status") == "available" and availability.get("role") == role:
                return worker_id
        return None
        
    def is_task_assigned(self, task_type: str, entity_id: str) -> bool:
        # Check if a task of a specific type is already assigned to an entity
        for task in self.task_queue:
            if task.get("type") == task_type and task.get(task_type + "_id") == entity_id:
                return True
        return False
        
    def update_task_status(self, task_id: str, status: str):
        # Update status of a task in the system
        for task in self.task_queue:
            if task.get("task_id") == task_id:
                task["status"] = status
                break