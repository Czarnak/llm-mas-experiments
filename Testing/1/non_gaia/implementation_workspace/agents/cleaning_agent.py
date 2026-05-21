from crewai import Agent, Task
from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime, timedelta

from models.animal_model import CleaningTask, Task
from utils.database import Database

class CleaningAgent(Agent):
    def __init__(self, database: Database):
        super().__init__(
            role="Cleaning Task Specialist",
            goal="Automatically generate daily cleaning tasks and on-demand tasks based on room conditions.",
            backstory="You are an expert in facility management and cleaning operations with deep understanding of shelter hygiene requirements.",
            verbose=True,
            allow_delegation=False,
            tools=[],
            database=database
        )
        
    def generate_daily_cleaning_tasks(self, rooms: List[str]) -> List[CleaningTask]:
        """Generate daily cleaning tasks for specified rooms"""
        tasks = []
        
        for room in rooms:
            # Create daily cleaning task
            task = CleaningTask(
                id=f"clean_daily_{room}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                room=room,
                type="dzienny",
                status="otwarte",
                assigned_to=None,
                deadline=datetime.now() + timedelta(hours=24),
                created_at=datetime.now()
            )
            
            # Save task
            self.database.save_cleaning_task(task)
            tasks.append(task)
            
        return tasks
        
    def generate_on_demand_cleaning_task(self, room: str, reason: str = "") -> CleaningTask:
        """Generate on-demand cleaning task"""
        # Create on-demand cleaning task
        task = CleaningTask(
            id=f"clean_on_demand_{room}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            room=room,
            type="na żądanie",
            status="otwarte",
            assigned_to=None,
            deadline=datetime.now() + timedelta(hours=4),
            created_at=datetime.now()
        )
        
        # Save task
        self.database.save_cleaning_task(task)
        return task
        
    def get_cleaning_tasks(self, status: str = None) -> List[CleaningTask]:
        """Get all cleaning tasks, optionally filtered by status"""
        all_tasks = self.database.get_all_cleaning_tasks()
        
        if status:
            return [task for task in all_tasks if task.status == status]
        
        return all_tasks
        
    def get_cleaning_task_by_id(self, task_id: str) -> CleaningTask:
        """Get a specific cleaning task by ID"""
        return self.database.get_cleaning_task(task_id)
        
    def update_cleaning_task_status(self, task_id: str, new_status: str) -> CleaningTask:
        """Update the status of a cleaning task"""
        task = self.database.get_cleaning_task(task_id)
        if task:
            task.status = new_status
            self.database.save_cleaning_task(task)
        return task
        
    def generate_cleaning_tasks_for_all_rooms(self) -> List[CleaningTask]:
        """Generate cleaning tasks for all rooms in the shelter"""
        # Define rooms in the shelter
        rooms = ["korytarz", "sala_glow", "sala_zwierzat", "kuchnia", "pokoj_weterynarza", "sala_wykladowa"]
        
        # Generate daily cleaning tasks for all rooms
        return self.generate_daily_cleaning_tasks(rooms)
        
    def generate_cleaning_tasks_from_tasks(self) -> List[Task]:
        """Generate cleaning tasks based on existing tasks that require cleaning"""
        # Get all open tasks
        all_tasks = self.database.get_all_tasks()
        open_tasks = [task for task in all_tasks if task.status == "otwarte"]
        
        tasks = []
        
        # For tasks that might require cleaning (like feeding, walks, etc.), create cleaning tasks
        for task in open_tasks:
            if task.type in ["karmienie", "spacer"]:
                # Create cleaning task for the area where the animal was handled
                room = "sala_zwierzat"  # Simplified for this example
                
                cleaning_task = CleaningTask(
                    id=f"clean_from_task_{task.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    room=room,
                    type="na żądanie",
                    status="otwarte",
                    assigned_to=None,
                    deadline=datetime.now() + timedelta(hours=2),
                    created_at=datetime.now()
                )
                
                # Save cleaning task
                self.database.save_cleaning_task(cleaning_task)
                tasks.append(cleaning_task)
                
        return tasks