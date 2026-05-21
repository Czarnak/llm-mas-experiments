from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Reservation(BaseModel):
    id: str = Field(..., description="Unique identifier for the reservation")
    user_id: str = Field(..., description="ID of the user who made the reservation")
    parking_lot_id: str = Field(..., description="ID of the parking lot")
    spot_id: str = Field(..., description="ID of the reserved parking spot")
    start_time: datetime = Field(..., description="Reservation start time")
    end_time: datetime = Field(..., description="Reservation end time")
    status: str = Field("confirmed", description="Reservation status: confirmed, cancelled, expired")
    cost: float = Field(..., description="Total cost of the reservation in PLN")
    created_at: datetime = Field(..., description="When the reservation was created")
    
    class Config:
        schema_extra = {
            "example": {
                "id": "res_001",
                "user_id": "user_123",
                "parking_lot_id": "parking_001",
                "spot_id": "spot_001",
                "start_time": "2023-05-15T10:00:00Z",
                "end_time": "2023-05-15T14:00:00Z",
                "status": "confirmed",
                "cost": 60.0,
                "created_at": "2023-05-15T09:00:00Z"
            }
        }


class ReservationRequest(BaseModel):
    user_id: str = Field(..., description="ID of the user requesting reservation")
    parking_lot_id: str = Field(..., description="ID of the parking lot")
    start_time: datetime = Field(..., description="Reservation start time")
    end_time: datetime = Field(..., description="Reservation end time")
    
    class Config:
        schema_extra = {
            "example": {
                "user_id": "user_123",
                "parking_lot_id": "parking_001",
                "start_time": "2023-05-15T10:00:00Z",
                "end_time": "2023-05-15T14:00:00Z"
            }
        }