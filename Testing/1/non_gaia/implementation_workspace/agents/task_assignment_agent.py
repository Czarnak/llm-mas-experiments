from crewai import Agent, Task
from pydantic import BaseModel
from typing import List, Dict, Any, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from models.animal_model import Task, TaskAssignment, StaffMember
    
from utils.database import Database

class TaskAssignmentAgent(Agent):
    def __init__(self, database: Database):
        super().__init__(
            role="Task Assignment Specialist",
            goal="Automatically assign tasks to available staff based on competencies, preferences, and current workload.",
            backstory="You are an expert in task allocation and resource management with deep understanding of shelter operations.",
            verbose=True,
            allow_delegation=False,
            tools=[],
            database=database
        )
        
    def assign_task(self, task_id: str, staff_members: List[str] = None) -> 'TaskAssignment':
        # Get the task
        task = self.database.get_task(task_id)
        if not task:
            return None
        
        # Get all staff members
        all_staff = self.database.get_all_staff()
        
        # If specific staff members are provided, filter them
        if staff_members:
            available_staff = [s for s in all_staff if s.id in staff_members]
        else:
            # Filter staff by role that can perform this task
            available_staff = self._filter_staff_by_task(task, all_staff)
            
        # Filter staff by availability
        available_staff = self._filter_staff_by_availability(available_staff, task)
        
        # If no available staff, return None
        if not available_staff:
            return None
        
        # Find the best staff member based on preferences, competencies, and workload
        best_staff = self._find_best_staff_member(task, available_staff)
        
        if best_staff:
            # Assign the task
            task.assigned_to = best_staff.id
            task.status = "w trakcie"
            
            # Update staff member's assigned tasks
            best_staff.assigned_tasks.append(task.id)
            
            # Save changes
            self.database.save_task(task)
            self.database.save_staff(best_staff)
            
            # Create assignment record
            assignment = TaskAssignment(
                task_id=task.id,
                staff_member_id=best_staff.id,
                assignment_date=datetime.now(),
                priority=task.priority
            )
            
            self.database.save_task_assignment(assignment)
            return assignment
        
        return None
        
    def _filter_staff_by_task(self, task: 'Task', staff_list: List['StaffMember']) -> List['StaffMember']:
        # Filter staff based on task type and their competencies
        filtered_staff = []
        
        for staff in staff_list:
            # Different tasks require different competencies
            if task.type == "karmienie":
                if "karmienie" in staff.competencies or staff.role == "opiekun":
                    filtered_staff.append(staff)
            elif task.type == "spacer":
                if "spacer" in staff.competencies or staff.role == "opiekun":
                    filtered_staff.append(staff)
            elif task.type == "szczepienie":
                if "szczepienie" in staff.competencies or staff.role == "weterynarz":
                    filtered_staff.append(staff)
            elif task.type == "sprzątanie":
                if "sprzątanie" in staff.competencies or staff.role == "sprzątacz":
                    filtered_staff.append(staff)
        
        return filtered_staff
        
    def _filter_staff_by_availability(self, staff_list: List['StaffMember'], task: 'Task') -> List['StaffMember']:
        # Filter staff by their availability for the task deadline
        available_staff = []
        
        for staff in staff_list:
            # Check if staff is available during the task deadline
            for slot in staff.availability:
                start_time = datetime.fromisoformat(slot.get("start"))
                end_time = datetime.fromisoformat(slot.get("end"))
                
                if start_time <= task.deadline <= end_time:
                    available_staff.append(staff)
                    break
        
        return available_staff
        
    def _find_best_staff_member(self, task: 'Task', staff_list: List['StaffMember']) -> 'StaffMember':
        # Find the best staff member based on:
        # 1. Competency match
        # 2. Preference match
        # 3. Current workload
        
        best_staff = None
        best_score = -1
        
        for staff in staff_list:
            score = 0
            
            # Check competency match
            if task.type == "karmienie" and "karmienie" in staff.competencies:
                score += 10
            elif task.type == "spacer" and "spacer" in staff.competencies:
                score += 10
            elif task.type == "szczepienie" and "szczepienie" in staff.competencies:
                score += 10
            elif task.type == "sprzątanie" and "sprzątanie" in staff.competencies:
                score += 10
            
            # Check preference match
            if task.type in staff.preferences:
                score += 5
            
            # Check current workload (lower is better)
            workload = len(staff.assigned_tasks)
            score -= workload
            
            # Update best staff if score is higher
            if score > best_score:
                best_score = score
                best_staff = staff
        
        return best_staff
        
    def auto_assign_all_tasks(self) -> List['TaskAssignment']:
        # Get all open tasks
        all_tasks = self.database.get_all_tasks()
        open_tasks = [task for task in all_tasks if task.status == "otwarte"]
        
        assignments = []
        
        for task in open_tasks:
            assignment = self.assign_task(task.id)
            if assignment:
                assignments.append(assignment)
                
        return assignments
        
    def get_task_assignments(self, task_id: str) -> 'TaskAssignment':
        return self.database.get_task_assignment(task_id)
        
    def get_staff_assignments(self, staff_id: str) -> List['TaskAssignment']:
        # Get all assignments for a specific staff member
        all_assignments = self.database.get_all_task_assignments()
        return [assignment for assignment in all_assignments if assignment.staff_member_id == staff_id]