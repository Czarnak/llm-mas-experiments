from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime


class Animal(BaseModel):
    id: str
    name: str
    species: str
    breed: str
    age: int
    health_status: str
    status: str  # "nakarmiony", "na spacerze", etc.
    admission_date: datetime
    vaccination_schedule: List[Dict[str, Any]]
    history: List[Dict[str, Any]]


class StaffMember(BaseModel):
    id: str
    name: str
    role: str  # "opiekun", "sprzątacz", "weterynarz"
    competencies: List[str]
    availability: List[Dict[str, Any]]
    preferences: List[str]
    assigned_tasks: List[str]


class Task(BaseModel):
    id: str
    type: str  # "karmienie", "spacer", "szczepienie", "sprzątanie"
    priority: str  # "krytyczne", "rutynowe"
    status: str  # "otwarte", "w trakcie", "zakończone"
    assigned_to: str  # staff member id
    animal_id: str
    deadline: datetime
    created_at: datetime
    completed_at: datetime = None


class TaskAssignment(BaseModel):
    task_id: str
    staff_member_id: str
    assignment_date: datetime
    priority: str


class VaccinationSchedule(BaseModel):
    animal_id: str
    vaccine_type: str
    scheduled_date: datetime
    completed: bool = False
    notes: str = ""


class CleaningTask(BaseModel):
    id: str
    room: str
    type: str  # "dzienny", "na żądanie"
    status: str  # "otwarte", "w trakcie", "zakończone"
    assigned_to: str = None
    deadline: datetime
    created_at: datetime


class AdoptionProcess(BaseModel):
    id: str
    animal_id: str
    applicant_name: str
    application_date: datetime
    status: str  # "wniosek", "rozpatrywanie", "zakończone"
    finalization_date: datetime = None


class EmergencyEvent(BaseModel):
    id: str
    type: str  # "nowe zwierzę", "nieobecność"
    description: str
    timestamp: datetime
    affected_animals: List[str]
    affected_staff: List[str]
    resolved: bool = False