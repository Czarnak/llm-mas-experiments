from crewai import Agent, Task
from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime

from models.animal_model import Animal, Task
from utils.database import Database

class AdmissionAgent(Agent):
    def __init__(self, database: Database):
        super().__init__(
            role="Animal Admission Specialist",
            goal="Manage the registration process for new animals, conduct initial health checks, and integrate them into the care schedule.",
            backstory="You are an expert in animal admissions with deep knowledge of shelter protocols and initial health assessments.",
            verbose=True,
            allow_delegation=False,
            tools=[],
            database=database
        )
        
    def register_new_animal(self, animal_data: Dict[str, Any]) -> Animal:
        # Create animal object
        animal = Animal(
            id=animal_data.get("id"),
            name=animal_data.get("name"),
            species=animal_data.get("species"),
            breed=animal_data.get("breed"),
            age=animal_data.get("age"),
            health_status=animal_data.get("health_status", "healthy"),
            status="nowe_zwierze",
            admission_date=datetime.now(),
            vaccination_schedule=[],
            history=[{
                "field": "admission",
                "old_value": None,
                "new_value": "registered",
                "timestamp": datetime.now()
            }]
        )
        
        # Save to database
        self.database.save_animal(animal)
        return animal
        
    def conduct_initial_health_check(self, animal_id: str) -> Dict[str, Any]:
        # Get animal
        animal = self.database.get_animal(animal_id)
        if not animal:
            return {}
        
        # Perform initial health check (simplified for this example)
        health_check_result = {
            "animal_id": animal_id,
            "check_date": datetime.now(),
            "health_status": animal.health_status,
            "notes": "Initial health check completed",
            "vaccination_needed": True if animal.age < 1 else False
        }
        
        # Update animal's health status
        animal.health_status = health_check_result["health_status"]
        
        # Add to history
        history_entry = {
            "field": "health_check",
            "old_value": None,
            "new_value": health_check_result,
            "timestamp": datetime.now()
        }
        animal.history.append(history_entry)
        
        # Save updated animal
        self.database.save_animal(animal)
        
        return health_check_result
        
    def integrate_into_care_schedule(self, animal_id: str) -> List[Task]:
        # Get animal
        animal = self.database.get_animal(animal_id)
        if not animal:
            return []
        
        # Create initial care tasks
        tasks = []
        
        # Create feeding task
        feeding_task = Task(
            id=f"feed_{animal_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            type="karmienie",
            priority="rutynowe",
            status="otwarte",
            assigned_to=None,
            animal_id=animal_id,
            deadline=datetime.now() + timedelta(hours=24),
            created_at=datetime.now()
        )
        
        self.database.save_task(feeding_task)
        tasks.append(feeding_task)
        
        # Create walk task
        walk_task = Task(
            id=f"walk_{animal_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            type="spacer",
            priority="rutynowe",
            status="otwarte",
            assigned_to=None,
            animal_id=animal_id,
            deadline=datetime.now() + timedelta(hours=12),
            created_at=datetime.now()
        )
        
        self.database.save_task(walk_task)
        tasks.append(walk_task)
        
        # Update animal status
        animal.status = "w_czasie_opieki"
        
        # Add to history
        history_entry = {
            "field": "status",
            "old_value": "nowe_zwierze",
            "new_value": "w_czasie_opieki",
            "timestamp": datetime.now()
        }
        animal.history.append(history_entry)
        
        # Save updated animal
        self.database.save_animal(animal)
        
        return tasks
        
    def process_admission(self, animal_data: Dict[str, Any]) -> Dict[str, Any]:
        # Register new animal
        animal = self.register_new_animal(animal_data)
        
        # Conduct initial health check
        health_check = self.conduct_initial_health_check(animal.id)
        
        # Integrate into care schedule
        care_tasks = self.integrate_into_care_schedule(animal.id)
        
        return {
            "animal": animal,
            "health_check": health_check,
            "care_tasks": care_tasks
        }
        
    def get_admitted_animals(self) -> List[Animal]:
        # Get all animals with "nowe_zwierze" status
        all_animals = self.database.get_all_animals()
        return [animal for animal in all_animals if animal.status == "nowe_zwierze"]