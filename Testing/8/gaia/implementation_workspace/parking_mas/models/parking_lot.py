from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ParkingLot(BaseModel):
    id: str = Field(..., description="Unique identifier for the parking lot")
    name: str = Field(..., description="Name of the parking lot")
    location: str = Field(..., description="Location of the parking lot")
    total_spaces: int = Field(..., description="Total number of parking spaces")
    available_spaces: int = Field(..., description="Number of available parking spaces")
    price_per_hour: float = Field(..., description="Price per hour for parking")
    is_available: bool = Field(True, description="Whether the parking lot is currently available")
    reservations: List[str] = Field(default_factory=list, description="List of reservation IDs")
    
    def reserve_space(self, reservation_id: str) -> bool:
        if self.available_spaces > 0:
            self.available_spaces -= 1
            self.reservations.append(reservation_id)
            return True
        return False
    
    def release_space(self, reservation_id: str) -> bool:
        if reservation_id in self.reservations:
            self.reservations.remove(reservation_id)
            self.available_spaces += 1
            return True
        return False
    
    def is_space_available(self) -> bool:
        return self.available_spaces > 0
    
    def get_cost(self, start_time: datetime, end_time: datetime) -> float:
        duration_hours = (end_time - start_time).total_seconds() / 3600
        return duration_hours * self.price_per_hour