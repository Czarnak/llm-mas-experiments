from crewai import Agent, Task
from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime, timedelta

from models.animal_model import Task
from utils.database import Database

class PriorityAgent(Agent):
    def __init__(self, database: Database):
        super().__init__(
            role="Task Priority Specialist",
            goal="Automatically distinguish critical tasks from routine tasks and dynamically update priorities based on situations.",
            backstory="You are an expert in task prioritization with deep understanding of shelter operations and emergency management.",
            verbose=True,
            allow_delegation=False,
            tools=[],
            database=database
        )
        
    def calculate_task_priority(self, task: Task) -> str:
        """Calculate priority based on task type, deadline, and other factors"""
        # Critical tasks based on type
        if task.type in ["szczepienie", "weterynarz"]:
            return "krytyczne"
        
        # Check deadline
        time_until_deadline = task.deadline - datetime.now()
        if time_until_deadline <= timedelta(hours=2):
            return "krytyczne"
        elif time_until_deadline <= timedelta(hours=12):
            return "wysoka"
        else:
            return "rutynowe"
        
    def update_task_priority(self, task_id: str) -> Task:
        """Update the priority of a specific task"""
        task = self.database.get_task(task_id)
        if not task:
            return None
        
        # Calculate new priority
        new_priority = self.calculate_task_priority(task)
        
        # Update if priority changed
        if task.priority != new_priority:
            old_priority = task.priority
            task.priority = new_priority
            
            # Add to history
            history_entry = {
                "field": "priority",
                "old_value": old_priority,
                "new_value": new_priority,
                "timestamp": datetime.now()
            }
            
            # Save updated task
            self.database.save_task(task)
            
        return task
        
    def update_all_task_priorities(self) -> List[Task]:
        """Update priorities for all tasks"""
        all_tasks = self.database.get_all_tasks()
        updated_tasks = []
        
        for task in all_tasks:
            updated_task = self.update_task_priority(task.id)
            if updated_task:
                updated_tasks.append(updated_task)
        
        return updated_tasks
        
    def get_priority_tasks(self, priority: str) -> List[Task]:
        """Get all tasks with a specific priority"""
        all_tasks = self.database.get_all_tasks()
        return [task for task in all_tasks if task.priority == priority]
        
    def get_critical_tasks(self) -> List[Task]:
        """Get all critical tasks"""
        return self.get_priority_tasks("krytyczne")
        
    def get_high_priority_tasks(self) -> List[Task]:
        """Get all high priority tasks"""
        return self.get_priority_tasks("wysoka")
        
    def get_routine_tasks(self) -> List[Task]:
        """Get all routine tasks"""
        return self.get_priority_tasks("rutynowe")
        
    def prioritize_emergency_tasks(self, emergency_tasks: List[Task]) -> List[Task]:
        """Set priority to critical for emergency tasks"""
        for task in emergency_tasks:
            task.priority = "krytyczne"
            self.database.save_task(task)
        
        return emergency_tasks
        
    def get_priority_summary(self) -> Dict[str, int]:
        """Get summary of tasks by priority"""
        all_tasks = self.database.get_all_tasks()
        
        summary = {
            "krytyczne": 0,
            "wysoka": 0,
            "rutynowe": 0
        }
        
        for task in all_tasks:
            summary[task.priority] += 1
            
        return summary