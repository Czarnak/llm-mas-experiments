from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, time


class ParkingLot(BaseModel):
    id: str = Field(..., description="Unique identifier for the parking lot")
    name: str = Field(..., description="Name of the parking lot")
    location: dict = Field(..., description="Geographic coordinates {lat, lng}")
    total_spots: int = Field(..., description="Total number of parking spots")
    available_spots: int = Field(..., description="Number of currently available parking spots")
    price_per_hour: float = Field(..., description="Price per hour in PLN")
    address: str = Field(..., description="Full address of the parking lot")
    opening_hours: dict = Field(..., description="Opening hours {start_time, end_time}")
    is_active: bool = Field(True, description="Whether the parking lot is currently active")
    
    class Config:
        schema_extra = {
            "example": {
                "id": "parking_001",
                "name": "Parking Lot A",
                "location": {"lat": 52.2297, "lng": 21.0122},
                "total_spots": 100,
                "available_spots": 45,
                "price_per_hour": 15.0,
                "address": "ul. Warszawska 15, Warsaw, Poland",
                "opening_hours": {"start_time": "08:00", "end_time": "22:00"},
                "is_active": True
            }
        }


class ParkingSpot(BaseModel):
    id: str = Field(..., description="Unique identifier for the parking spot")
    parking_lot_id: str = Field(..., description="ID of the parking lot this spot belongs to")
    spot_number: str = Field(..., description="Number/identifier of the parking spot")
    is_available: bool = Field(True, description="Whether the spot is currently available")
    
    class Config:
        schema_extra = {
            "example": {
                "id": "spot_001",
                "parking_lot_id": "parking_001",
                "spot_number": "A1",
                "is_available": True
            }
        }