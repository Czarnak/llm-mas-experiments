from crewai import Agent, Task
from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime

from models.animal_model import AdoptionProcess, Animal
from utils.database import Database

class AdoptionAgent(Agent):
    def __init__(self, database: Database):
        super().__init__(
            role="Adoption Process Specialist",
            goal="Manage the adoption process from application submission to finalization.",
            backstory="You are an expert in animal adoption processes with deep understanding of shelter regulations and adoption procedures.",
            verbose=True,
            allow_delegation=False,
            tools=[],
            database=database
        )
        
    def submit_adoption_application(self, animal_id: str, applicant_name: str, application_data: Dict[str, Any]) -> AdoptionProcess:
        """Submit an adoption application for an animal"""
        # Create adoption process
        process = AdoptionProcess(
            id=f"adoption_{animal_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            animal_id=animal_id,
            applicant_name=applicant_name,
            application_date=datetime.now(),
            status="wniosek",
            finalization_date=None
        )
        
        # Save process
        self.database.save_adoption_process(process)
        return process
        
    def review_application(self, process_id: str) -> AdoptionProcess:
        """Review an adoption application"""
        process = self.database.get_adoption_process(process_id)
        if process:
            process.status = "rozpatrywanie"
            self.database.save_adoption_process(process)
        return process
        
    def approve_application(self, process_id: str) -> AdoptionProcess:
        """Approve an adoption application"""
        process = self.database.get_adoption_process(process_id)
        if process:
            process.status = "zakończone"
            process.finalization_date = datetime.now()
            
            # Update animal status
            animal = self.database.get_animal(process.animal_id)
            if animal:
                animal.status = "w_adopcji"
                animal.history.append({
                    "field": "status",
                    "old_value": animal.status,
                    "new_value": "w_adopcji",
                    "timestamp": datetime.now()
                })
                self.database.save_animal(animal)
            
            self.database.save_adoption_process(process)
        return process
        
    def reject_application(self, process_id: str, reason: str = "") -> AdoptionProcess:
        """Reject an adoption application"""
        process = self.database.get_adoption_process(process_id)
        if process:
            process.status = "odrzucony"
            self.database.save_adoption_process(process)
        return process
        
    def finalize_adoption(self, process_id: str) -> AdoptionProcess:
        """Finalize adoption process"""
        process = self.database.get_adoption_process(process_id)
        if process:
            process.status = "zakończone"
            process.finalization_date = datetime.now()
            
            # Update animal status
            animal = self.database.get_animal(process.animal_id)
            if animal:
                animal.status = "w_adopcji"
                animal.history.append({
                    "field": "status",
                    "old_value": animal.status,
                    "new_value": "w_adopcji",
                    "timestamp": datetime.now()
                })
                self.database.save_animal(animal)
            
            self.database.save_adoption_process(process)
        return process
        
    def get_adoption_process(self, process_id: str) -> AdoptionProcess:
        """Get a specific adoption process"""
        return self.database.get_adoption_process(process_id)
        
    def get_animal_adoption_processes(self, animal_id: str) -> List[AdoptionProcess]:
        """Get all adoption processes for a specific animal"""
        all_processes = self.database.get_all_adoption_processes()
        return [p for p in all_processes if p.animal_id == animal_id]
        
    def get_all_adoption_processes(self) -> List[AdoptionProcess]:
        """Get all adoption processes"""
        return self.database.get_all_adoption_processes()
        
    def get_pending_applications(self) -> List[AdoptionProcess]:
        """Get all pending adoption applications"""
        all_processes = self.database.get_all_adoption_processes()
        return [p for p in all_processes if p.status == "wniosek"]
        
    def get_in_review_applications(self) -> List[AdoptionProcess]:
        """Get all applications in review"""
        all_processes = self.database.get_all_adoption_processes()
        return [p for p in all_processes if p.status == "rozpatrywanie"]
        
    def get_completed_adoptions(self) -> List[AdoptionProcess]:
        """Get all completed adoptions"""
        all_processes = self.database.get_all_adoption_processes()
        return [p for p in all_processes if p.status == "zakończone"]
        
    def get_adoption_summary(self) -> Dict[str, int]:
        """Get summary of adoption processes by status"""
        all_processes = self.database.get_all_adoption_processes()
        
        summary = {}
        for process in all_processes:
            if process.status not in summary:
                summary[process.status] = 0
            summary[process.status] += 1
            
        return summary