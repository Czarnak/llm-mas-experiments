from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class StaffMember:
    id: str
    name: str
    role: str  # "caretaker", "cleaner", "veterinarian", "volunteer"
    skills: List[str] = field(default_factory=list)
    preferences: Dict[str, str] = field(default_factory=dict)
    availability: List[Dict] = field(default_factory=list)
    current_tasks: List[str] = field(default_factory=list)
    
    def add_availability_slot(self, start_time: datetime, end_time: datetime):
        self.availability.append({
            "start": start_time,
            "end": end_time
        })
        
    def remove_availability_slot(self, start_time: datetime, end_time: datetime):
        self.availability = [slot for slot in self.availability 
                           if not (slot["start"] == start_time and slot["end"] == end_time)]
        
    def add_task(self, task_id: str):
        self.current_tasks.append(task_id)
        
    def remove_task(self, task_id: str):
        if task_id in self.current_tasks:
            self.current_tasks.remove(task_id)
        
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "skills": self.skills,
            "preferences": self.preferences,
            "availability": self.availability,
            "current_tasks": self.current_tasks
        }

    @classmethod
    def from_dict(cls, data: Dict):
        staff = cls(
            id=data["id"],
            name=data["name"],
            role=data["role"],
            skills=data.get("skills", []),
            preferences=data.get("preferences", {}),
            availability=data.get("availability", []),
            current_tasks=data.get("current_tasks", [])
        )
        return staff