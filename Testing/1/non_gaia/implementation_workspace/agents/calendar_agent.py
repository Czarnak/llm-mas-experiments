from crewai import Agent, Task
from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime, timedelta

from models.animal_model import VaccinationSchedule, Task
from utils.database import Database

class CalendarAgent(Agent):
    def __init__(self, database: Database):
        super().__init__(
            role="Calendar and Scheduling Specialist",
            goal="Automatically plan and monitor vaccination windows and generate appropriate tasks for staff.",
            backstory="You are an expert in scheduling and calendar management with deep knowledge of veterinary care timelines.",
            verbose=True,
            allow_delegation=False,
            tools=[],
            database=database
        )
        
    def create_vaccination_schedule(self, animal_id: str, vaccine_type: str, days_until_next: int = 30) -> VaccinationSchedule:
        # Create vaccination schedule
        schedule = VaccinationSchedule(
            animal_id=animal_id,
            vaccine_type=vaccine_type,
            scheduled_date=datetime.now() + timedelta(days=days_until_next),
            completed=False,
            notes=f"Planowane szczepienie: {vaccine_type}"
        )
        
        # Save schedule
        self.database.save_vaccination_schedule(schedule)
        return schedule
        
    def update_vaccination_schedule(self, animal_id: str, updates: Dict[str, Any]) -> VaccinationSchedule:
        # Get existing schedule
        schedule = self.database.get_vaccination_schedule(animal_id)
        if not schedule:
            return None
        
        # Update fields
        for key, value in updates.items():
            if hasattr(schedule, key):
                setattr(schedule, key, value)
                
        # Save updated schedule
        self.database.save_vaccination_schedule(schedule)
        return schedule
        
    def get_vaccination_schedule(self, animal_id: str) -> VaccinationSchedule:
        return self.database.get_vaccination_schedule(animal_id)
        
    def get_overdue_vaccinations(self) -> List[VaccinationSchedule]:
        # Get all vaccination schedules
        all_schedules = self.database.get_all_vaccination_schedules()
        
        # Find overdue vaccinations
        overdue = []
        current_time = datetime.now()
        
        for schedule in all_schedules:
            if not schedule.completed and schedule.scheduled_date < current_time:
                overdue.append(schedule)
                
        return overdue
        
    def get_upcoming_vaccinations(self, days_ahead: int = 7) -> List[VaccinationSchedule]:
        # Get all vaccination schedules
        all_schedules = self.database.get_all_vaccination_schedules()
        
        # Find upcoming vaccinations
        upcoming = []
        current_time = datetime.now()
        future_time = current_time + timedelta(days=days_ahead)
        
        for schedule in all_schedules:
            if not schedule.completed and current_time <= schedule.scheduled_date <= future_time:
                upcoming.append(schedule)
                
        return upcoming
        
    def generate_vaccination_tasks(self) -> List[Task]:
        # Generate tasks for overdue vaccinations
        overdue = self.get_overdue_vaccinations()
        
        tasks = []
        for schedule in overdue:
            # Create task for vaccination
            task = Task(
                id=f"vaccinate_{schedule.animal_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                type="szczepienie",
                priority="krytyczne",
                status="otwarte",
                assigned_to=None,
                animal_id=schedule.animal_id,
                deadline=schedule.scheduled_date,
                created_at=datetime.now()
            )
            
            # Save task
            self.database.save_task(task)
            tasks.append(task)
            
        return tasks
        
    def generate_reminder_tasks(self) -> List[Task]:
        # Generate reminder tasks for upcoming vaccinations
        upcoming = self.get_upcoming_vaccinations(3)  # 3 days ahead
        
        tasks = []
        for schedule in upcoming:
            # Create reminder task
            task = Task(
                id=f"reminder_{schedule.animal_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                type="przypomnienie",
                priority="rutynowe",
                status="otwarte",
                assigned_to=None,
                animal_id=schedule.animal_id,
                deadline=schedule.scheduled_date - timedelta(days=1),
                created_at=datetime.now()
            )
            
            # Save task
            self.database.save_task(task)
            tasks.append(task)
            
        return tasks
        
    def generate_all_calendar_tasks(self) -> List[Task]:
        # Generate all vaccination-related tasks
        overdue_tasks = self.generate_vaccination_tasks()
        reminder_tasks = self.generate_reminder_tasks()
        
        return overdue_tasks + reminder_tasks