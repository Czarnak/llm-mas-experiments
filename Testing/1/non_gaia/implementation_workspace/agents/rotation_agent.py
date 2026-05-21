from crewai import Agent, Task
from pydantic import BaseModel
from typing import List, Dict, Any, TYPE_CHECKING
from datetime import datetime, timedelta

if TYPE_CHECKING:
    from models.animal_model import Task, TaskAssignment, StaffMember
    
from utils.database import Database

class RotationAgent(Agent):
    def __init__(self, database: Database):
        super().__init__(
            role="Task Rotation Specialist",
            goal="Ensure fair distribution of tasks among animals and staff, maintaining balanced workload distribution.",
            backstory="You are an expert in workload balancing and fair distribution with deep understanding of shelter operations.",
            verbose=True,
            allow_delegation=False,
            tools=[],
            database=database
        )
        
    def calculate_workload_balance(self, staff_id: str) -> Dict[str, Any]:
        """Calculate workload balance for a specific staff member"""
        # Get staff member
        staff = self.database.get_staff(staff_id)
        if not staff:
            return {}
        
        # Get all assignments for this staff member
        all_assignments = self.database.get_all_task_assignments()
        staff_assignments = [a for a in all_assignments if a.staff_member_id == staff_id]
        
        # Count tasks by type
        task_counts = {}
        for assignment in staff_assignments:
            task = self.database.get_task(assignment.task_id)
            if task:
                task_type = task.type
                if task_type not in task_counts:
                    task_counts[task_type] = 0
                task_counts[task_type] += 1
        
        return {
            "staff_id": staff_id,
            "total_tasks": len(staff_assignments),
            "task_distribution": task_counts,
            "balance_score": self._calculate_balance_score(task_counts)
        }
        
    def _calculate_balance_score(self, task_counts: Dict[str, int]) -> float:
        """Calculate a balance score based on task distribution"""
        if not task_counts:
            return 1.0
        
        # Get all task types
        task_types = list(task_counts.keys())
        
        # Calculate average tasks per type
        total_tasks = sum(task_counts.values())
        if total_tasks == 0:
            return 1.0
        
        avg_tasks = total_tasks / len(task_types)
        
        # Calculate variance (lower is better)
        variance = sum((count - avg_tasks) ** 2 for count in task_counts.values()) / len(task_types)
        
        # Balance score (0-1, where 1 is perfectly balanced)
        balance_score = 1.0 / (1.0 + variance)
        
        return balance_score
        
    def get_staff_balance_scores(self) -> List[Dict[str, Any]]:
        """Get balance scores for all staff members"""
        all_staff = self.database.get_all_staff()
        scores = []
        
        for staff in all_staff:
            score = self.calculate_workload_balance(staff.id)
            scores.append(score)
        
        return scores
        
    def get_underutilized_staff(self, min_tasks: int = 5) -> List['StaffMember']:
        """Get staff members with below average task count"""
        all_staff = self.database.get_all_staff()
        underutilized = []
        
        # Calculate average tasks
        all_assignments = self.database.get_all_task_assignments()
        total_assignments = len(all_assignments)
        total_staff = len(all_staff)
        avg_tasks = total_assignments / total_staff if total_staff > 0 else 0
        
        for staff in all_staff:
            staff_assignments = [a for a in all_assignments if a.staff_member_id == staff.id]
            if len(staff_assignments) < min_tasks:
                underutilized.append(staff)
        
        return underutilized
        
    def get_overutilized_staff(self, max_tasks: int = 15) -> List['StaffMember']:
        """Get staff members with above average task count"""
        all_staff = self.database.get_all_staff()
        overutilized = []
        
        # Calculate average tasks
        all_assignments = self.database.get_all_task_assignments()
        total_assignments = len(all_assignments)
        total_staff = len(all_staff)
        avg_tasks = total_assignments / total_staff if total_staff > 0 else 0
        
        for staff in all_staff:
            staff_assignments = [a for a in all_assignments if a.staff_member_id == staff.id]
            if len(staff_assignments) > max_tasks:
                overutilized.append(staff)
        
        return overutilized
        
    def balance_workload(self) -> List[Dict[str, Any]]:
        """Attempt to balance workload across staff"""
        # Get all staff and their balance scores
        staff_scores = self.get_staff_balance_scores()
        
        # Identify underutilized and overutilized staff
        underutilized = self.get_underutilized_staff()
        overutilized = self.get_overutilized_staff()
        
        # For simplicity, let's just return the current state
        return {
            "staff_balance_scores": staff_scores,
            "underutilized_staff": [s.id for s in underutilized],
            "overutilized_staff": [s.id for s in overutilized]
        }
        
    def ensure_animal_task_balance(self, animal_id: str) -> Dict[str, Any]:
        """Ensure fair distribution of tasks for a specific animal"""
        # Get all tasks for this animal
        all_tasks = self.database.get_all_tasks()
        animal_tasks = [task for task in all_tasks if task.animal_id == animal_id]
        
        # Count tasks by type
        task_counts = {}
        for task in animal_tasks:
            task_type = task.type
            if task_type not in task_counts:
                task_counts[task_type] = 0
            task_counts[task_type] += 1
        
        # Calculate balance score
        total_tasks = sum(task_counts.values())
        if total_tasks > 0:
            avg_tasks = total_tasks / len(task_counts) if task_counts else 0
            variance = sum((count - avg_tasks) ** 2 for count in task_counts.values()) / len(task_counts)
            balance_score = 1.0 / (1.0 + variance)
        else:
            balance_score = 1.0
        
        return {
            "animal_id": animal_id,
            "task_distribution": task_counts,
            "balance_score": balance_score,
            "total_tasks": total_tasks
        }
        
    def get_animal_task_balances(self) -> List[Dict[str, Any]]:
        """Get task balance for all animals"""
        all_animals = self.database.get_all_animals()
        balances = []
        
        for animal in all_animals:
            balance = self.ensure_animal_task_balance(animal.id)
            balances.append(balance)
        
        return balances