from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class Truck(BaseModel):
    id: str = Field(..., description="Unique identifier for the truck")
    location: str = Field(..., description="Current location of the truck")
    capacity: int = Field(..., description="Maximum capacity of the truck in liters")
    current_load: int = Field(..., description="Current load in liters")
    status: str = Field(default="free", description="Status of the truck: free, busy, full")
    assigned_container: Optional[str] = Field(None, description="ID of container assigned to this truck")
    last_maintenance: Optional[datetime] = Field(None, description="Timestamp of last maintenance")
    
    def is_full(self, threshold: float = 0.9) -> bool:
        """Check if truck is full based on threshold"""
        return self.current_load >= self.capacity * threshold
    
    def is_overfill(self, threshold: float = 0.95) -> bool:
        """Check if truck is overfilled"""
        return self.current_load >= self.capacity * threshold
    
    def assign_container(self, container_id: str):
        """Assign a container to this truck"""
        self.assigned_container = container_id
        self.status = "busy"
    
    def complete_task(self):
        """Complete the assigned task and reset"""
        self.assigned_container = None
        self.status = "free"
    
    def load_waste(self, amount: int):
        """Load waste into the truck"""
        self.current_load += amount
        if self.is_full():
            self.status = "full"
        elif self.is_overfill():
            self.status = "full"
        else:
            self.status = "busy"
