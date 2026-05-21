from typing import Dict, Any, List
from dataclasses import dataclass
from enum import Enum
import asyncio


class TaskType(str, Enum):
    CLEAN = "clean"
    FEED = "feed"
    WALK = "walk"
    VACCINATION = "vaccination"
    INITIAL_CHECKUP = "initial_checkup"
    HEALTH = "health"
    ADOPTION = "adoption"


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    CANCELLED = "cancelled"


class WorkerRole(str, Enum):
    CARETAKER = "caretaker"
    CLEANER = "cleaner"
    VETERINARIAN = "veterinarian"


class AnimalState(str, Enum):
    HUNGRY = "hungry"
    FED = "fed"
    NEEDS_WALK = "needs_walk"
    WALKED = "walked"
    HEALTHY = "healthy"
    SICK = "sick"
    AVAILABLE = "available"
    ADOPTED = "adopted"


class RoomState(str, Enum):
    DIRTY = "dirty"
    CLEAN = "clean"


class WorkerAvailability:
    def __init__(self, worker_id: str, status: str, role: WorkerRole, shift: str = "morning"):
        self.worker_id = worker_id
        self.status = status  # available, unavailable, on_break
        self.role = role
        self.shift = shift
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "worker_id": self.worker_id,
            "status": self.status,
            "role": self.role.value,
            "shift": self.shift
        }


class Task:
    def __init__(self, task_id: str, task_type: TaskType, assigned_to: str, status: TaskStatus = TaskStatus.PENDING):
        self.task_id = task_id
        self.task_type = task_type
        self.assigned_to = assigned_to
        self.status = status
        self.created_at = "2023-01-01T00:00:00Z"
        self.updated_at = "2023-01-01T00:00:00Z"
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "task_type": self.task_type.value,
            "assigned_to": self.assigned_to,
            "status": self.status.value,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


class ServiceLayer:
    def __init__(self):
        self.tasks = {}
        self.workers = {}
        self.animals = {}
        self.rooms = {}
        self.adoption_applications = {}
        
    def create_task(self, task_id: str, task_type: TaskType, assigned_to: str) -> Task:
        """Create a new task"""
        task = Task(task_id, task_type, assigned_to)
        self.tasks[task_id] = task
        return task
        
    def assign_task(self, task_id: str, assigned_to: str) -> bool:
        """Assign a task to a worker"""
        if task_id in self.tasks:
            task = self.tasks[task_id]
            task.assigned_to = assigned_to
            task.status = TaskStatus.IN_PROGRESS
            return True
        return False
        
    def complete_task(self, task_id: str) -> bool:
        """Complete a task"""
        if task_id in self.tasks:
            task = self.tasks[task_id]
            task.status = TaskStatus.DONE
            task.updated_at = "2023-01-01T00:00:00Z"  # In real system, would use current timestamp
            return True
        return False
        
    def get_available_workers(self, role: WorkerRole) -> List[str]:
        """Get list of available workers for a specific role"""
        available_workers = []
        for worker_id, worker_info in self.workers.items():
            if worker_info["status"] == "available" and worker_info["role"] == role.value:
                available_workers.append(worker_id)
        return available_workers
        
    def update_worker_availability(self, worker_id: str, status: str, role: WorkerRole):
        """Update worker availability"""
        self.workers[worker_id] = {
            "status": status,
            "role": role.value
        }
        
    def get_animal_state(self, animal_id: str) -> Dict[str, Any]:
        """Get current state of an animal"""
        if animal_id in self.animals:
            return self.animals[animal_id]
        return {}
        
    def update_animal_state(self, animal_id: str, state_key: str, state_value: str):
        """Update state of an animal"""
        if animal_id not in self.animals:
            self.animals[animal_id] = {}
        self.animals[animal_id][state_key] = state_value
        
    def get_room_state(self, room_id: str) -> str:
        """Get current state of a room"""
        if room_id in self.rooms:
            return self.rooms[room_id]
        return "unknown"
        
    def update_room_state(self, room_id: str, state: str):
        """Update state of a room"""
        self.rooms[room_id] = state
        
    def create_adoption_application(self, application_id: str, animal_id: str, applicant_id: str) -> Dict[str, Any]:
        """Create a new adoption application"""
        application = {
            "application_id": application_id,
            "animal_id": animal_id,
            "applicant_id": applicant_id,
            "status": "pending",
            "created_at": "2023-01-01T00:00:00Z"
        }
        self.adoption_applications[application_id] = application
        return application
        
    def process_adoption_application(self, application_id: str) -> bool:
        """Process an adoption application"""
        if application_id in self.adoption_applications:
            application = self.adoption_applications[application_id]
            application["status"] = "approved"
            # Update animal adoption status
            self.update_animal_state(application["animal_id"], "adoption_status", "adopted")
            return True
        return False