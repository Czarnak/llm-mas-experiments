from crewai import Agent, Task
from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime

from models.animal_model import EmergencyEvent, Task, TaskAssignment
from utils.database import Database

class EmergencyAgent(Agent):
    def __init__(self, database: Database):
        super().__init__(
            role="Emergency Response Specialist",
            goal="Instantly reconfigure schedules in case of emergencies such as new animal admissions or staff unavailability.",
            backstory="You are an expert in emergency management and crisis response with deep understanding of shelter operations.",
            verbose=True,
            allow_delegation=False,
            tools=[],
            database=database
        )
        
    def report_emergency(self, emergency_type: str, description: str, affected_animals: List[str] = None, affected_staff: List[str] = None) -> EmergencyEvent:
        """Report an emergency event"""
        # Create emergency event
        event = EmergencyEvent(
            id=f"emergency_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            type=emergency_type,
            description=description,
            timestamp=datetime.now(),
            affected_animals=affected_animals or [],
            affected_staff=affected_staff or [],
            resolved=False
        )
        
        # Save event
        self.database.save_emergency(event)
        return event
        
    def handle_new_animal_emergency(self, animal_id: str) -> List[Task]:
        """Handle emergency of new animal admission"""
        # Report emergency
        emergency = self.report_emergency(
            emergency_type="nowe_zwierze",
            description=f"Nowe zwierzę: {animal_id} zostało przyjęte w awarii",
            affected_animals=[animal_id]
        )
        
        # Get animal
        animal = self.database.get_animal(animal_id)
        if not animal:
            return []
        
        # Create emergency tasks
        tasks = []
        
        # Create feeding task
        feeding_task = Task(
            id=f"emergency_feed_{animal_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            type="karmienie",
            priority="krytyczne",
            status="otwarte",
            assigned_to=None,
            animal_id=animal_id,
            deadline=datetime.now() + timedelta(hours=2),
            created_at=datetime.now()
        )
        
        self.database.save_task(feeding_task)
        tasks.append(feeding_task)
        
        # Create health check task
        health_task = Task(
            id=f"emergency_health_{animal_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            type="weterynarz",
            priority="krytyczne",
            status="otwarte",
            assigned_to=None,
            animal_id=animal_id,
            deadline=datetime.now() + timedelta(hours=4),
            created_at=datetime.now()
        )
        
        self.database.save_task(health_task)
        tasks.append(health_task)
        
        return tasks
        
    def handle_staff_unavailability_emergency(self, staff_id: str) -> List[Task]:
        """Handle emergency of staff unavailability"""
        # Report emergency
        emergency = self.report_emergency(
            emergency_type="nieobecność",
            description=f"Pracownik: {staff_id} jest nieobecny w awarii",
            affected_staff=[staff_id]
        )
        
        # Get staff member
        staff = self.database.get_staff(staff_id)
        if not staff:
            return []
        
        # Get all tasks assigned to this staff member
        all_assignments = self.database.get_all_task_assignments()
        staff_assignments = [a for a in all_assignments if a.staff_member_id == staff_id]
        
        # Get tasks that need to be reassigned
        tasks_to_reassign = []
        for assignment in staff_assignments:
            task = self.database.get_task(assignment.task_id)
            if task and task.status == "w trakcie":
                tasks_to_reassign.append(task)
                
        # Update task status to open for reassignment
        for task in tasks_to_reassign:
            task.status = "otwarte"
            task.assigned_to = None
            self.database.save_task(task)
            
        return tasks_to_reassign
        
    def resolve_emergency(self, event_id: str) -> EmergencyEvent:
        """Resolve an emergency event"""
        event = self.database.get_emergency(event_id)
        if event:
            event.resolved = True
            event.timestamp = datetime.now()
            self.database.save_emergency(event)
        return event
        
    def get_active_emergencies(self) -> List[EmergencyEvent]:
        """Get all unresolved emergencies"""
        all_emergencies = self.database.get_all_emergencies()
        return [e for e in all_emergencies if not e.resolved]
        
    def get_emergency_by_id(self, event_id: str) -> EmergencyEvent:
        """Get a specific emergency event"""
        return self.database.get_emergency(event_id)
        
    def reconfigure_schedule_for_emergency(self, emergency_type: str, **kwargs) -> Dict[str, Any]:
        """Reconfigure schedule based on emergency type"""
        if emergency_type == "nowe_zwierze":
            return {
                "tasks": self.handle_new_animal_emergency(kwargs.get("animal_id")),
                "emergency": self.report_emergency("nowe_zwierze", "Emergency new animal admission")
            }
        elif emergency_type == "nieobecność":
            return {
                "tasks": self.handle_staff_unavailability_emergency(kwargs.get("staff_id")),
                "emergency": self.report_emergency("nieobecność", "Emergency staff unavailability")
            }
        else:
            return {}
        
    def get_emergency_summary(self) -> Dict[str, int]:
        """Get summary of emergencies by type"""
        all_emergencies = self.database.get_all_emergencies()
        
        summary = {}
        for event in all_emergencies:
            if event.type not in summary:
                summary[event.type] = 0
            summary[event.type] += 1
            
        return summary