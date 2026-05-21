import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Any

# Import required libraries
from crewai import Agent, Task, Crew
from pydantic import BaseModel

# Create project structure
os.makedirs("agents", exist_ok=True)
os.makedirs("models", exist_ok=True)
os.makedirs("utils", exist_ok=True)

# Define the main system structure
print("Creating animal shelter management system...")

# Define data models

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

print("Data models created successfully.")

# Import agents
from agents.animal_registry_agent import AnimalRegistryAgent
from agents.staff_management_agent import StaffManagementAgent
from agents.task_generation_agent import TaskGenerationAgent
from agents.task_assignment_agent import TaskAssignmentAgent
from agents.calendar_agent import CalendarAgent
from agents.cleaning_agent import CleaningAgent
from agents.admission_agent import AdmissionAgent
from agents.priority_agent import PriorityAgent
from agents.rotation_agent import RotationAgent
from agents.emergency_agent import EmergencyAgent
from agents.adoption_agent import AdoptionAgent

# Import database
from utils.database import Database

# Create a main system class

class AnimalShelterSystem:
    def __init__(self):
        # Initialize database
        self.database = Database("data")
        
        # Initialize agents
        self.animal_registry_agent = AnimalRegistryAgent(self.database)
        self.staff_management_agent = StaffManagementAgent(self.database)
        self.task_generation_agent = TaskGenerationAgent(self.database)
        self.task_assignment_agent = TaskAssignmentAgent(self.database)
        self.calendar_agent = CalendarAgent(self.database)
        self.cleaning_agent = CleaningAgent(self.database)
        self.admission_agent = AdmissionAgent(self.database)
        self.priority_agent = PriorityAgent(self.database)
        self.rotation_agent = RotationAgent(self.database)
        self.emergency_agent = EmergencyAgent(self.database)
        self.adoption_agent = AdoptionAgent(self.database)
        
        print("Animal Shelter Management System initialized with all agents.")
        
    def run_demo(self):
        """Run a demonstration of the system functionality"""
        print("\n=== ANIMAL SHELTER MANAGEMENT SYSTEM DEMO ===\n")
        
        # 1. Add staff members
        print("1. Adding staff members...")
        staff_members = [
            {
                "id": "staff_001",
                "name": "Jan Kowalski",
                "role": "opiekun",
                "competencies": ["karmienie", "spacer", "weterynarz"],
                "availability": [
                    {"start": datetime.now().isoformat(), "end": (datetime.now() + timedelta(hours=8)).isoformat()}
                ],
                "preferences": ["karmienie", "spacer"]
            },
            {
                "id": "staff_002",
                "name": "Anna Nowak",
                "role": "weterynarz",
                "competencies": ["weterynarz", "szczepienie"],
                "availability": [
                    {"start": datetime.now().isoformat(), "end": (datetime.now() + timedelta(hours=8)).isoformat()}
                ],
                "preferences": ["weterynarz"]
            },
            {
                "id": "staff_003",
                "name": "Piotr Wiśniewski",
                "role": "sprzątacz",
                "competencies": ["sprzątanie"],
                "availability": [
                    {"start": datetime.now().isoformat(), "end": (datetime.now() + timedelta(hours=8)).isoformat()}
                ],
                "preferences": ["sprzątanie"]
            }
        ]
        
        for staff_data in staff_members:
            self.staff_management_agent.add_staff_member(staff_data)
        
        print("   Staff members added successfully.")
        
        # 2. Add animals
        print("\n2. Adding animals...")
        animals = [
            {
                "id": "animal_001",
                "name": "Burek",
                "species": "pies",
                "breed": "kundel",
                "age": 2,
                "health_status": "zdrowy",
                "status": "nowe_zwierze"
            },
            {
                "id": "animal_002",
                "name": "Miauczek",
                "species": "kot",
                "breed": "brytyjski",
                "age": 1,
                "health_status": "zdrowy",
                "status": "nowe_zwierze"
            }
        ]
        
        for animal_data in animals:
            self.animal_registry_agent.add_animal(animal_data)
        
        print("   Animals added successfully.")
        
        # 3. Process animal admission
        print("\n3. Processing animal admission...")
        admission_result = self.admission_agent.process_admission(animals[0])
        print("   Animal admission completed.")
        
        # 4. Generate tasks
        print("\n4. Generating tasks...")
        tasks = self.task_generation_agent.generate_all_tasks()
        print(f"   Generated {len(tasks)} tasks.")
        
        # 5. Assign tasks
        print("\n5. Assigning tasks...")
        assignments = self.task_assignment_agent.auto_assign_all_tasks()
        print(f"   Assigned {len(assignments)} tasks.")
        
        # 6. Generate cleaning tasks
        print("\n6. Generating cleaning tasks...")
        cleaning_tasks = self.cleaning_agent.generate_cleaning_tasks_for_all_rooms()
        print(f"   Generated {len(cleaning_tasks)} cleaning tasks.")
        
        # 7. Generate vaccination schedule
        print("\n7. Generating vaccination schedule...")
        vaccination_schedule = self.calendar_agent.create_vaccination_schedule("animal_001", "podstawowa", 30)
        print("   Vaccination schedule created.")
        
        # 8. Generate vaccination tasks
        print("\n8. Generating vaccination tasks...")
        vaccine_tasks = self.calendar_agent.generate_all_calendar_tasks()
        print(f"   Generated {len(vaccine_tasks)} vaccination tasks.")
        
        # 9. Update task priorities
        print("\n9. Updating task priorities...")
        self.priority_agent.update_all_task_priorities()
        priority_summary = self.priority_agent.get_priority_summary()
        print(f"   Priority summary: {priority_summary}")
        
        # 10. Check workload balance
        print("\n10. Checking workload balance...")
        balance = self.rotation_agent.balance_workload()
        print("   Workload balance checked.")
        
        # 11. Handle emergency
        print("\n11. Handling emergency situation...")
        emergency_tasks = self.emergency_agent.handle_new_animal_emergency("animal_002")
        print(f"   Emergency handled. Generated {len(emergency_tasks)} emergency tasks.")
        
        # 12. Process adoption
        print("\n12. Processing adoption application...")
        adoption_process = self.adoption_agent.submit_adoption_application(
            "animal_001", "Jan Nowak", {"address": "ul. Testowa 1, Warszawa"}
        )
        print("   Adoption application submitted.")
        
        # Summary
        print("\n=== DEMO COMPLETE ===")
        print("System successfully demonstrated all required functionality:")
        print("- Animal registry management")
        print("- Staff management")
        print("- Task generation and assignment")
        print("- Calendar and vaccination management")
        print("- Cleaning task generation")
        print("- Animal admission process")
        print("- Task prioritization")
        print("- Fair task rotation")
        print("- Emergency response")
        print("- Adoption process")

# Initialize the system
system = AnimalShelterSystem()

# Create the main entry point
if __name__ == "__main__":
    print("Animal Shelter Management System ready to run.")
    print("Run with: python animal_shelter_system.py")
    
    # Run demo
    try:
        system.run_demo()
    except Exception as e:
        print(f"Error during demo execution: {e}")
        import traceback
        traceback.print_exc()