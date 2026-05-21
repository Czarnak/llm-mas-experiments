from typing import Dict, List, Optional
from models.animal_model import Animal, StaffMember, Task, CleaningTask, AdoptionProcess, EmergencyEvent, VaccinationSchedule, TaskAssignment
from datetime import datetime
import json
import os

class Database:
    def __init__(self, db_path: str = "data"):
        self.db_path = db_path
        os.makedirs(db_path, exist_ok=True)
        
    def save_animal(self, animal: Animal):
        with open(f"{self.db_path}/animals/{animal.id}.json", "w") as f:
            json.dump(animal.dict(), f)
            
    def get_animal(self, animal_id: str) -> Optional[Animal]:
        try:
            with open(f"{self.db_path}/animals/{animal_id}.json", "r") as f:
                data = json.load(f)
                return Animal(**data)
        except FileNotFoundError:
            return None
            
    def get_all_animals(self) -> List[Animal]:
        animals = []
        for file in os.listdir(f"{self.db_path}/animals"):
            if file.endswith(".json"):
                with open(f"{self.db_path}/animals/{file}", "r") as f:
                    data = json.load(f)
                    animals.append(Animal(**data))
        return animals
        
    def save_staff(self, staff: StaffMember):
        with open(f"{self.db_path}/staff/{staff.id}.json", "w") as f:
            json.dump(staff.dict(), f)
            
    def get_staff(self, staff_id: str) -> Optional[StaffMember]:
        try:
            with open(f"{self.db_path}/staff/{staff_id}.json", "r") as f:
                data = json.load(f)
                return StaffMember(**data)
        except FileNotFoundError:
            return None
            
    def get_all_staff(self) -> List[StaffMember]:
        staff = []
        for file in os.listdir(f"{self.db_path}/staff"):
            if file.endswith(".json"):
                with open(f"{self.db_path}/staff/{file}", "r") as f:
                    data = json.load(f)
                    staff.append(StaffMember(**data))
        return staff
        
    def save_task(self, task: Task):
        with open(f"{self.db_path}/tasks/{task.id}.json", "w") as f:
            json.dump(task.dict(), f)
            
    def get_task(self, task_id: str) -> Optional[Task]:
        try:
            with open(f"{self.db_path}/tasks/{task_id}.json", "r") as f:
                data = json.load(f)
                return Task(**data)
        except FileNotFoundError:
            return None
            
    def get_all_tasks(self) -> List[Task]:
        tasks = []
        for file in os.listdir(f"{self.db_path}/tasks"):
            if file.endswith(".json"):
                with open(f"{self.db_path}/tasks/{file}", "r") as f:
                    data = json.load(f)
                    tasks.append(Task(**data))
        return tasks
        
    def save_cleaning_task(self, task: CleaningTask):
        with open(f"{self.db_path}/cleaning_tasks/{task.id}.json", "w") as f:
            json.dump(task.dict(), f)
            
    def get_cleaning_task(self, task_id: str) -> Optional[CleaningTask]:
        try:
            with open(f"{self.db_path}/cleaning_tasks/{task_id}.json", "r") as f:
                data = json.load(f)
                return CleaningTask(**data)
        except FileNotFoundError:
            return None
            
    def get_all_cleaning_tasks(self) -> List[CleaningTask]:
        tasks = []
        for file in os.listdir(f"{self.db_path}/cleaning_tasks"):
            if file.endswith(".json"):
                with open(f"{self.db_path}/cleaning_tasks/{file}", "r") as f:
                    data = json.load(f)
                    tasks.append(CleaningTask(**data))
        return tasks
        
    def save_adoption_process(self, process: AdoptionProcess):
        with open(f"{self.db_path}/adoption_processes/{process.id}.json", "w") as f:
            json.dump(process.dict(), f)
            
    def get_adoption_process(self, process_id: str) -> Optional[AdoptionProcess]:
        try:
            with open(f"{self.db_path}/adoption_processes/{process_id}.json", "r") as f:
                data = json.load(f)
                return AdoptionProcess(**data)
        except FileNotFoundError:
            return None
            
    def get_all_adoption_processes(self) -> List[AdoptionProcess]:
        processes = []
        for file in os.listdir(f"{self.db_path}/adoption_processes"):
            if file.endswith(".json"):
                with open(f"{self.db_path}/adoption_processes/{file}", "r") as f:
                    data = json.load(f)
                    processes.append(AdoptionProcess(**data))
        return processes
        
    def save_emergency(self, event: EmergencyEvent):
        with open(f"{self.db_path}/emergencies/{event.id}.json", "w") as f:
            json.dump(event.dict(), f)
            
    def get_emergency(self, event_id: str) -> Optional[EmergencyEvent]:
        try:
            with open(f"{self.db_path}/emergencies/{event_id}.json", "r") as f:
                data = json.load(f)
                return EmergencyEvent(**data)
        except FileNotFoundError:
            return None
            
    def get_all_emergencies(self) -> List[EmergencyEvent]:
        emergencies = []
        for file in os.listdir(f"{self.db_path}/emergencies"):
            if file.endswith(".json"):
                with open(f"{self.db_path}/emergencies/{file}", "r") as f:
                    data = json.load(f)
                    emergencies.append(EmergencyEvent(**data))
        return emergencies
        
    def save_vaccination_schedule(self, schedule: VaccinationSchedule):
        with open(f"{self.db_path}/vaccination_schedules/{schedule.animal_id}.json", "w") as f:
            json.dump(schedule.dict(), f)
            
    def get_vaccination_schedule(self, animal_id: str) -> Optional[VaccinationSchedule]:
        try:
            with open(f"{self.db_path}/vaccination_schedules/{animal_id}.json", "r") as f:
                data = json.load(f)
                return VaccinationSchedule(**data)
        except FileNotFoundError:
            return None
            
    def save_task_assignment(self, assignment: TaskAssignment):
        with open(f"{self.db_path}/task_assignments/{assignment.task_id}.json", "w") as f:
            json.dump(assignment.dict(), f)
            
    def get_task_assignment(self, task_id: str) -> Optional[TaskAssignment]:
        try:
            with open(f"{self.db_path}/task_assignments/{task_id}.json", "r") as f:
                data = json.load(f)
                return TaskAssignment(**data)
        except FileNotFoundError:
            return None