from typing import Dict, Any, Optional
from .base_agent import BaseAgent, AgentMessage
from ..models.task import Task


class TaskTrackingAgent(BaseAgent):
    def __init__(self, agent_id: str, name: str):
        super().__init__(agent_id, name)
        self.tasks: Dict[str, Task] = {}
        
    def process_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        if message.protocol == "UpdateTaskStatus":
            return self._update_task_status(message)
        elif message.protocol == "SetTaskPriority":
            return self._set_task_priority(message)
        else:
            # Handle unknown protocols
            return None
    
    def _update_task_status(self, message: AgentMessage) -> Optional[AgentMessage]:
        task_id = message.content.get("TaskID")
        status_report = message.content.get("StatusReport")
        
        if not task_id or not status_report:
            return None
        
        task = self.tasks.get(task_id)
        if not task:
            return None
        
        # Update task status
        task.update_status(status_report.get("status"), status_report.get("timestamp"))
        
        # Return confirmation
        return AgentMessage(
            sender=self.agent_id,
            receiver=message.sender,
            protocol="StatusUpdateConfirmation",
            content={"Success": True},
            timestamp=0.0
        )
    
    def _set_task_priority(self, message: AgentMessage) -> Optional[AgentMessage]:
        task_id = message.content.get("TaskID")
        priority_level = message.content.get("PriorityLevel")
        
        if not task_id or not priority_level:
            return None
        
        task = self.tasks.get(task_id)
        if not task:
            return None
        
        # Update task priority
        task.priority = priority_level
        
        # Return confirmation
        return AgentMessage(
            sender=self.agent_id,
            receiver=message.sender,
            protocol="PriorityUpdateConfirmation",
            content={"Success": True},
            timestamp=0.0
        )
    
    def get_capabilities(self) -> Dict[str, Any]:
        return {
            "roles": ["TaskStatusTracker", "TaskPriorityManager"],
            "protocols": ["UpdateTaskStatus", "SetTaskPriority"],
            "permissions": {
                "read": ["TaskID", "StatusReport", "PriorityLevel"],
                "write": ["TaskID", "StatusReport", "PriorityLevel"],
                "consume": ["TaskID", "StatusReport", "PriorityLevel"],
                "produce": ["StatusUpdateConfirmation", "PriorityUpdateConfirmation"]
            }
        }
    
    def register_task(self, task: Task):
        self.tasks[task.id] = task
        
    def get_task(self, task_id: str) -> Optional[Task]:
        return self.tasks.get(task_id)
    
    def get_all_tasks(self) -> Dict[str, Task]:
        return self.tasks