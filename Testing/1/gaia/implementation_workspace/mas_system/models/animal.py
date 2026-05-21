from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class Animal:
    id: str
    name: str
    species: str
    breed: str
    age: int
    gender: str
    status: str = "available"  # available, in_care, adopted, etc.
    health_status: str = "healthy"  # healthy, sick, recovering, etc.
    vaccination_status: Dict[str, datetime] = field(default_factory=dict)
    adoption_status: str = "pending"  # pending, approved, completed
    admission_date: datetime = field(default_factory=datetime.now)
    care_history: List[Dict] = field(default_factory=list)
    preferences: Dict[str, str] = field(default_factory=dict)
    
    def add_care_event(self, event_type: str, details: str, timestamp: datetime = None):
        if timestamp is None:
            timestamp = datetime.now()
        self.care_history.append({
            "type": event_type,
            "details": details,
            "timestamp": timestamp
        })
        
    def update_status(self, new_status: str):
        self.status = new_status
        self.add_care_event("status_update", f"Status changed to {new_status}")
        
    def add_vaccination(self, vaccine_name: str, date: datetime):
        self.vaccination_status[vaccine_name] = date
        self.add_care_event("vaccination", f"Vaccinated with {vaccine_name}")
        
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "species": self.species,
            "breed": self.breed,
            "age": self.age,
            "gender": self.gender,
            "status": self.status,
            "health_status": self.health_status,
            "vaccination_status": self.vaccination_status,
            "adoption_status": self.adoption_status,
            "admission_date": self.admission_date.isoformat(),
            "care_history": self.care_history,
            "preferences": self.preferences
        }

    @classmethod
    def from_dict(cls, data: Dict):
        animal = cls(
            id=data["id"],
            name=data["name"],
            species=data["species"],
            breed=data["breed"],
            age=data["age"],
            gender=data["gender"],
            status=data.get("status", "available"),
            health_status=data.get("health_status", "healthy"),
            vaccination_status=data.get("vaccination_status", {}),
            adoption_status=data.get("adoption_status", "pending"),
            admission_date=datetime.fromisoformat(data["admission_date"]),
            care_history=data.get("care_history", []),
            preferences=data.get("preferences", {})
        )
        return animal