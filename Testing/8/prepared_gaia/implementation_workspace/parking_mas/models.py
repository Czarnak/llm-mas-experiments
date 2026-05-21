from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class Localization(BaseModel):
    latitude: float
    longitude: float
    radius_km: float = 2.0


class ReservationTimeslot(BaseModel):
    start_time: datetime
    end_time: datetime


class ParkingSpot(BaseModel):
    parking_id: str
    name: str
    location: Localization
    total_spots: int
    price_per_hour: float
    min_price: float
    reservations: List[str] = []


class Reservation(BaseModel):
    reservation_id: str
    user_id: str
    parking_id: str
    timeslot: ReservationTimeslot
    status: str = "active"


class ConsolidatedOffer(BaseModel):
    parking_id: str
    name: str
    location: Localization
    available_spots: int
    price_per_hour: float
    reservation_id: Optional[str] = None


class User(BaseModel):
    user_id: str
    name: str


class ParkingAgentState(BaseModel):
    parking_id: str
    name: str
    location: Localization
    total_spots: int
    price_per_hour: float
    min_price: float
    reservations: List[Reservation] = []
