from crewai import Agent, Task
from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime

from models.animal_model import StaffMember
from utils.database import Database

class StaffManagementAgent(Agent):
    def __init__(self, database: Database):
        super().__init__(
            role="Staff Management Coordinator",
            goal="Manage staff accounts, roles, competencies, limits, and preferences.",
            backstory="You are an expert in human resources and staff management with deep knowledge of shelter operations.",
            verbose=True,
            allow_delegation=False,
            tools=[],
            database=database
        )
        
    def add_staff_member(self, staff_data: Dict[str, Any]) -> StaffMember:
        # Create staff member object
        staff = StaffMember(
            id=staff_data.get("id"),
            name=staff_data.get("name"),
            role=staff_data.get("role"),
            competencies=staff_data.get("competencies", []),
            availability=staff_data.get("availability", []),
            preferences=staff_data.get("preferences", []),
            assigned_tasks=[]
        )
        
        # Save to database
        self.database.save_staff(staff)
        return staff
        
    def update_staff_member(self, staff_id: str, updates: Dict[str, Any]) -> StaffMember:
        # Retrieve staff member
        staff = self.database.get_staff(staff_id)
        
        # Update fields
        for key, value in updates.items():
            if hasattr(staff, key):
                setattr(staff, key, value)
                
        # Save updated staff member
        self.database.save_staff(staff)
        return staff
        
    def get_staff_by_id(self, staff_id: str) -> StaffMember:
        return self.database.get_staff(staff_id)
        
    def get_all_staff(self) -> List[StaffMember]:
        return self.database.get_all_staff()
        
    def get_staff_by_role(self, role: str) -> List[StaffMember]:
        all_staff = self.get_all_staff()
        return [staff for staff in all_staff if staff.role == role]
        
    def update_availability(self, staff_id: str, new_availability: List[Dict[str, Any]]) -> StaffMember:
        staff = self.database.get_staff(staff_id)
        staff.availability = new_availability
        self.database.save_staff(staff)
        return staff
        
    def add_competency(self, staff_id: str, competency: str) -> StaffMember:
        staff = self.database.get_staff(staff_id)
        if competency not in staff.competencies:
            staff.competencies.append(competency)
        self.database.save_staff(staff)
        return staff
        
    def remove_competency(self, staff_id: str, competency: str) -> StaffMember:
        staff = self.database.get_staff(staff_id)
        if competency in staff.competencies:
            staff.competencies.remove(competency)
        self.database.save_staff(staff)
        return staff
        
    def add_preference(self, staff_id: str, preference: str) -> StaffMember:
        staff = self.database.get_staff(staff_id)
        if preference not in staff.preferences:
            staff.preferences.append(preference)
        self.database.save_staff(staff)
        return staff
        
    def remove_preference(self, staff_id: str, preference: str) -> StaffMember:
        staff = self.database.get_staff(staff_id)
        if preference in staff.preferences:
            staff.preferences.remove(preference)
        self.database.save_staff(staff)
        return staff