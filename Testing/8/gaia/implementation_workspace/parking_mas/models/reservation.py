from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Reservation(BaseModel):
    id: str = Field(..., description="Unique identifier for the reservation")
    user_id: str = Field(..., description="ID of the user who made the reservation")
    parking_lot_id: str = Field(..., description="ID of the parking lot")
    start_time: datetime = Field(..., description="Start time of the reservation")
    end_time: datetime = Field(..., description="End time of the reservation")
    status: str = Field("reserved", description="Status of the reservation: reserved, cancelled, completed")
    cost: float = Field(..., description="Total cost of the reservation")
    payment_status: str = Field("pending", description="Payment status: pending, paid, failed")
    
    def extend_reservation(self, new_end_time: datetime) -> bool:
        if new_end_time > self.end_time:
            self.end_time = new_end_time
            return True
        return False
    
    def modify_reservation_time(self, new_start_time: datetime, new_end_time: datetime) -> bool:
        if new_start_time < new_end_time:
            self.start_time = new_start_time
            self.end_time = new_end_time
            return True
        return False