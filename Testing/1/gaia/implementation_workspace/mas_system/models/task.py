from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class Task:
    id: str
    task_type: str  # "feeding", "cleaning", "vaccination", "walking", "adoption"
    animal_id: str
    assigned_to: Optional[str] = None
    status: str = "pending"  # pending, in_progress, completed, cancelled
    priority: str = "normal"  # low, normal, high, critical
    created_at: datetime = field(default_factory=datetime.now)
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    details: Dict[str, str] = field(default_factory=dict)
    
    def update_status(self, new_status: str, timestamp: datetime = None):
        if timestamp is None:
            timestamp = datetime.now()
        self.status = new_status
        if new_status == "completed":
            self.completed_at = timestamp
        
    def assign_to(self, staff_id: str):
        self.assigned_to = staff_id
        
    def to_dict(self):
        return {
            "id": self.id,
            "task_type": self.task_type,
            "animal_id": self.animal_id,
            "assigned_to": self.assigned_to,
            "status": self.status,
            "priority": self.priority,
            "created_at": self.created_at.isoformat(),
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "details": self.details
        }

    @classmethod
    def from_dict(cls, data: Dict):
        task = cls(
            id=data["id"],
            task_type=data["task_type"],
            animal_id=data["animal_id"],
            assigned_to=data.get("assigned_to"),
            status=data.get("status", "pending"),
            priority=data.get("priority", "normal"),
            created_at=datetime.fromisoformat(data["created_at"]),
            due_date=datetime.fromisoformat(data["due_date"]) if data.get("due_date") else None,
            completed_at=datetime.fromisoformat(data["completed_at"]) if data.get("completed_at") else None,
            details=data.get("details", {})
        )
        return task