from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Container(BaseModel):
    id: str = Field(..., description="Unique identifier for the container")
    location: str = Field(..., description="Geographic location of the container")
    capacity: int = Field(..., description="Maximum capacity of the container in liters")
    current_fill_level: int = Field(..., description="Current fill level in liters")
    last_empty_time: Optional[datetime] = Field(None, description="Timestamp when container was last emptied")
    status: str = Field(default="normal", description="Status of the container: normal, full, warning")
    
    def is_full(self, threshold: float = 0.9) -> bool:
        """Check if container is full based on threshold"""
        return self.current_fill_level >= self.capacity * threshold
    
    def is_overfill(self, threshold: float = 0.95) -> bool:
        """Check if container is overfilled"""
        return self.current_fill_level >= self.capacity * threshold
    
    def update_fill_level(self, new_level: int):
        """Update the fill level of the container"""
        self.current_fill_level = new_level
        if self.is_full():
            self.status = "warning"
        elif self.is_overfill():
            self.status = "full"
        else:
            self.status = "normal"

    def empty(self):
        """Empty the container"""
        self.current_fill_level = 0
        self.last_empty_time = datetime.now()
        self.status = "normal"
