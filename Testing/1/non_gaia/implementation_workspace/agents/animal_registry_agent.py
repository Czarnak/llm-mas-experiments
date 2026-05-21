from crewai import Agent, Task
from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime

from models.animal_model import Animal
from utils.database import Database

class AnimalRegistryAgent(Agent):
    def __init__(self, database: Database):
        super().__init__(
            role="Animal Registry Manager",
            goal="Manage the digital registry of animals, including adding, editing, and tracking health status, statuses, and event history.",
            backstory="You are an expert in animal record management with extensive experience in veterinary and shelter operations.",
            verbose=True,
            allow_delegation=False,
            tools=[],
            database=database
        )
        
    def add_animal(self, animal_data: Dict[str, Any]) -> Animal:
        # Create animal object
        animal = Animal(
            id=animal_data.get("id"),
            name=animal_data.get("name"),
            species=animal_data.get("species"),
            breed=animal_data.get("breed"),
            age=animal_data.get("age"),
            health_status=animal_data.get("health_status", "healthy"),
            status=animal_data.get("status", "unknown"),
            admission_date=datetime.now(),
            vaccination_schedule=[],
            history=[]
        )
        
        # Save to database
        self.database.save_animal(animal)
        return animal
        
    def update_animal(self, animal_id: str, updates: Dict[str, Any]) -> Animal:
        # Retrieve animal
        animal = self.database.get_animal(animal_id)
        
        # Update fields
        for key, value in updates.items():
            if hasattr(animal, key):
                setattr(animal, key, value)
                
        # Add to history
        history_entry = {
            "field": key,
            "old_value": getattr(animal, key),
            "new_value": value,
            "timestamp": datetime.now()
        }
        animal.history.append(history_entry)
        
        # Save updated animal
        self.database.save_animal(animal)
        return animal
        
    def get_animal_status(self, animal_id: str) -> str:
        animal = self.database.get_animal(animal_id)
        return animal.status
        
    def update_animal_status(self, animal_id: str, new_status: str) -> Animal:
        animal = self.database.get_animal(animal_id)
        old_status = animal.status
        animal.status = new_status
        
        # Add to history
        history_entry = {
            "field": "status",
            "old_value": old_status,
            "new_value": new_status,
            "timestamp": datetime.now()
        }
        animal.history.append(history_entry)
        
        self.database.save_animal(animal)
        return animal
        
    def get_animal_health_status(self, animal_id: str) -> str:
        animal = self.database.get_animal(animal_id)
        return animal.health_status
        
    def update_animal_health_status(self, animal_id: str, new_health_status: str) -> Animal:
        animal = self.database.get_animal(animal_id)
        old_health_status = animal.health_status
        animal.health_status = new_health_status
        
        # Add to history
        history_entry = {
            "field": "health_status",
            "old_value": old_health_status,
            "new_value": new_health_status,
            "timestamp": datetime.now()
        }
        animal.history.append(history_entry)
        
        self.database.save_animal(animal)
        return animal

    def get_animal_history(self, animal_id: str) -> List[Dict[str, Any]]:
        animal = self.database.get_animal(animal_id)
        return animal.history

    def get_all_animals(self) -> List[Animal]:
        return self.database.get_all_animals()

    def get_animal_by_id(self, animal_id: str) -> Animal:
        return self.database.get_animal(animal_id)