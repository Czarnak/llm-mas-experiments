from crewai import Agent, Task
from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime, timedelta

from models.animal_model import Task, VaccinationSchedule
from utils.database import Database

class TaskGenerationAgent(Agent):
    def __init__(self, database: Database):
        super().__init__(
            role="Task Generation Specialist",
            goal="Automatically generate tasks for feeding, walks, vaccinations, and cleaning based on animal needs and schedules.",
            backstory="You are an expert in shelter operations and task planning with deep understanding of animal care requirements.",
            verbose=True,
            allow_delegation=False,
            tools=[],
            database=database
        )
        
    def generate_feeding_tasks(self, animal_id: str) -> List[Task]:
        # Get animal
        animal = self.database.get_animal(animal_id)
        if not animal:
            return []
        
        # Create feeding task
        task = Task(
            id=f"feed_{animal_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            type="karmienie",
            priority="rutynowe",
            status="otwarte",
            assigned_to=None,
            animal_id=animal_id,
            deadline=datetime.now() + timedelta(hours=24),
            created_at=datetime.now()
        )
        
        # Save task
        self.database.save_task(task)
        return [task]
        
    def generate_walk_tasks(self, animal_id: str) -> List[Task]:
        # Get animal
        animal = self.database.get_animal(animal_id)
        if not animal:
            return []
        
        # Create walk task
        task = Task(
            id=f"walk_{animal_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            type="spacer",
            priority="rutynowe",
            status="otwarte",
            assigned_to=None,
            animal_id=animal_id,
            deadline=datetime.now() + timedelta(hours=12),
            created_at=datetime.now()
        )
        
        # Save task
        self.database.save_task(task)
        return [task]
        
    def generate_vaccination_tasks(self, animal_id: str) -> List[Task]:
        # Get animal
        animal = self.database.get_animal(animal_id)
        if not animal:
            return []
        
        # Check vaccination schedule
        schedule = self.database.get_vaccination_schedule(animal_id)
        
        # If no schedule, create one
        if not schedule:
            # Create a basic vaccination schedule
            schedule = VaccinationSchedule(
                animal_id=animal_id,
                vaccine_type="podstawowa",
                scheduled_date=datetime.now() + timedelta(days=30),
                completed=False,
                notes="Pierwsze szczepienie"
            )
            self.database.save_vaccination_schedule(schedule)
        
        # Create vaccination task
        task = Task(
            id=f"vaccinate_{animal_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            type="szczepienie",
            priority="krytyczne",
            status="otwarte",
            assigned_to=None,
            animal_id=animal_id,
            deadline=schedule.scheduled_date,
            created_at=datetime.now()
        )
        
        # Save task
        self.database.save_task(task)
        return [task]
        
    def generate_cleaning_tasks(self, room: str, type: str = "dzienny") -> List[Task]:
        # Create cleaning task
        task = Task(
            id=f"clean_{room}_{type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            type="sprzątanie",
            priority="rutynowe",
            status="otwarte",
            assigned_to=None,
            animal_id=None,
            deadline=datetime.now() + timedelta(hours=24),
            created_at=datetime.now()
        )
        
        # Save task
        self.database.save_task(task)
        return [task]
        
    def generate_task(self, task_type: str, animal_id: str = None, room: str = None) -> List[Task]:
        if task_type == "karmienie":
            return self.generate_feeding_tasks(animal_id)
        elif task_type == "spacer":
            return self.generate_walk_tasks(animal_id)
        elif task_type == "szczepienie":
            return self.generate_vaccination_tasks(animal_id)
        elif task_type == "sprzątanie":
            return self.generate_cleaning_tasks(room)
        else:
            return []
        
    def generate_all_tasks(self) -> List[Task]:
        # Generate all types of tasks for all animals
        all_tasks = []
        animals = self.database.get_all_animals()
        
        for animal in animals:
            # Generate feeding task
            feeding_tasks = self.generate_feeding_tasks(animal.id)
            all_tasks.extend(feeding_tasks)
            
            # Generate walk task
            walk_tasks = self.generate_walk_tasks(animal.id)
            all_tasks.extend(walk_tasks)
            
            # Generate vaccination task
            vaccine_tasks = self.generate_vaccination_tasks(animal.id)
            all_tasks.extend(vaccine_tasks)
            
        return all_tasks