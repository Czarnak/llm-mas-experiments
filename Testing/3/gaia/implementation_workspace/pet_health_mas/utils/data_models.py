from pydantic import BaseModel
from typing import Optional, Dict, Any


class PetData(BaseModel):
    pet_id: str
    name: str
    species: str
    breed: str
    age: int
    weight: float
    

class PhysiologicalData(BaseModel):
    pet_id: str
    heart_rate: int
    temperature: float
    respiratory_rate: int
    blood_pressure: str
    timestamp: str
    

class LocationData(BaseModel):
    pet_id: str
    latitude: float
    longitude: float
    timestamp: str
    

class BehaviorData(BaseModel):
    pet_id: str
    activity_level: str
    behavior_patterns: str
    timestamp: str
    

class HealthStatus(BaseModel):
    pet_id: str
    status: str  # normal, warning, critical
    description: str
    timestamp: str
    

class AlertData(BaseModel):
    pet_id: str
    alert_type: str  # health, location, behavior
    message: str
    severity: str  # low, medium, high
    timestamp: str
    

class AppointmentRequest(BaseModel):
    pet_id: str
    vet_id: str
    appointment_type: str
    date: str
    time: str
    notes: str
    

class AppointmentConfirmation(BaseModel):
    pet_id: str
    appointment_id: str
    vet_id: str
    date: str
    time: str
    status: str  # confirmed, pending, cancelled
    

class ReminderData(BaseModel):
    pet_id: str
    appointment_id: str
    reminder_type: str  # appointment, vaccination, checkup
    message: str
    reminder_date: str
    reminder_time: str
    

class CommunicationMessage(BaseModel):
    sender: str
    receiver: str
    protocol: str
    data: Dict[str, Any]
    timestamp: str
    