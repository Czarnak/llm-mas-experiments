from typing import Dict, Any, Optional
from .base_agent import BaseAgent, AgentMessage
from ..models.task import Task


class TaskGenerationAgent(BaseAgent):
    def __init__(self, agent_id: str, name: str):
        super().__init__(agent_id, name)
        self.tasks: Dict[str, Task] = {}
        self.task_counter = 0
        
    def process_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        if message.protocol == "GenerateCareTask":
            return self._generate_care_task(message)
        elif message.protocol == "ScheduleVaccination":
            return self._schedule_vaccination(message)
        elif message.protocol == "GenerateCleaningTask":
            return self._generate_cleaning_task(message)
        else:
            # Handle unknown protocols
            return None
    
    def _generate_care_task(self, message: AgentMessage) -> Optional[AgentMessage]:
        task_definition = message.content.get("TaskDefinition")
        if not task_definition:
            return None
        
        # Create task instance
        self.task_counter += 1
        task_id = f"task_{self.task_counter}"
        
        task = Task(
            id=task_id,
            task_type=task_definition["type"],
            animal_id=task_definition["animal_id"],
            priority=task_definition.get("priority", "normal"),
            details=task_definition.get("details", {})
        )
        
        # Store task
        self.tasks[task.id] = task
        
        # Return task ID
        return AgentMessage(
            sender=self.agent_id,
            receiver=message.sender,
            protocol="TaskID",
            content={"TaskID": task.id},
            timestamp=0.0
        )
    
    def _schedule_vaccination(self, message: AgentMessage) -> Optional[AgentMessage]:
        animal_id = message.content.get("AnimalID")
        vaccination_plan = message.content.get("VaccinationPlan")
        
        if not animal_id or not vaccination_plan:
            return None
        
        # Create vaccination task
        self.task_counter += 1
        task_id = f"vaccination_{self.task_counter}"
        
        task = Task(
            id=task_id,
            task_type="vaccination",
            animal_id=animal_id,
            details={"vaccine": vaccination_plan.get("vaccine"), "due_date": vaccination_plan.get("due_date")}
        )
        
        # Store task
        self.tasks[task.id] = task
        
        # Return vaccination task ID
        return AgentMessage(
            sender=self.agent_id,
            receiver=message.sender,
            protocol="VaccinationTaskID",
            content={"VaccinationTaskID": task.id},
            timestamp=0.0
        )
    
    def _generate_cleaning_task(self, message: AgentMessage) -> Optional[AgentMessage]:
        cleaning_requirements = message.content.get("CleaningRequirements")
        if not cleaning_requirements:
            return None
        
        # Create cleaning task
        self.task_counter += 1
        task_id = f"cleaning_{self.task_counter}"
        
        task = Task(
            id=task_id,
            task_type="cleaning",
            animal_id=cleaning_requirements.get("animal_id"),
            details={"room": cleaning_requirements.get("room"), "type": cleaning_requirements.get("type")}
        )
        
        # Store task
        self.tasks[task.id] = task
        
        # Return cleaning task ID
        return AgentMessage(
            sender=self.agent_id,
            receiver=message.sender,
            protocol="CleaningTaskID",
            content={"CleaningTaskID": task.id},
            timestamp=0.0
        )
    
    def get_capabilities(self) -> Dict[str, Any]:
        return {
            "roles": ["TaskGenerator", "VaccinationScheduler", "CleaningTaskGenerator"],
            "protocols": ["GenerateCareTask", "ScheduleVaccination", "GenerateCleaningTask"],
            "permissions": {
                "read": ["TaskDefinition", "AnimalID", "VaccinationPlan", "CleaningRequirements"],
                "write": ["TaskDefinition", "AnimalID", "VaccinationPlan", "CleaningRequirements"],
                "consume": ["TaskDefinition", "AnimalID", "VaccinationPlan", "CleaningRequirements"],
                "produce": ["TaskID", "VaccinationTaskID", "CleaningTaskID"]
            }
        }
    
    def get_task(self, task_id: str) -> Optional[Task]:
        return self.tasks.get(task_id)
    
    def get_all_tasks(self) -> Dict[str, Task]:
        return self.tasks