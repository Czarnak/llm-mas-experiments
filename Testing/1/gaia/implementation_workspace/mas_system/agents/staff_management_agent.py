from typing import Dict, Any, Optional
from .base_agent import BaseAgent, AgentMessage
from ..models.staff import StaffMember


class StaffManagementAgent(BaseAgent):
    def __init__(self, agent_id: str, name: str):
        super().__init__(agent_id, name)
        self.staff: Dict[str, StaffMember] = {}
        
    def process_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        if message.protocol == "UpdateStaffAvailability":
            return self._update_staff_availability(message)
        elif message.protocol == "AllocateTask":
            return self._allocate_task(message)
        else:
            # Handle unknown protocols
            return None
    
    def _update_staff_availability(self, message: AgentMessage) -> Optional[AgentMessage]:
        staff_id = message.content.get("StaffID")
        availability_slot = message.content.get("AvailabilitySlot")
        
        if not staff_id or not availability_slot:
            return None
        
        staff = self.staff.get(staff_id)
        if not staff:
            return None
        
        # Add availability slot
        staff.add_availability_slot(
            availability_slot["start"],
            availability_slot["end"]
        )
        
        # Return confirmation
        return AgentMessage(
            sender=self.agent_id,
            receiver=message.sender,
            protocol="AvailabilityConfirmation",
            content={"Success": True},
            timestamp=0.0
        )
    
    def _allocate_task(self, message: AgentMessage) -> Optional[AgentMessage]:
        task_id = message.content.get("TaskID")
        staff_preferences = message.content.get("StaffPreferences")
        
        if not task_id or not staff_preferences:
            return None
        
        # In a real implementation, this would implement the task allocation logic
        # For now, we'll just return a confirmation
        return AgentMessage(
            sender=self.agent_id,
            receiver=message.sender,
            protocol="AssignmentConfirmation",
            content={"TaskID": task_id, "Assigned": True},
            timestamp=0.0
        )
    
    def get_capabilities(self) -> Dict[str, Any]:
        return {
            "roles": ["StaffMember", "TaskAllocator"],
            "protocols": ["UpdateStaffAvailability", "AllocateTask"],
            "permissions": {
                "read": ["StaffID", "AvailabilitySlot", "TaskID", "StaffPreferences"],
                "write": ["StaffID", "AvailabilitySlot", "TaskID", "StaffPreferences"],
                "consume": ["StaffID", "AvailabilitySlot", "TaskID", "StaffPreferences"],
                "produce": ["AvailabilityConfirmation", "AssignmentConfirmation"]
            }
        }
    
    def register_staff(self, staff: StaffMember):
        self.staff[staff.id] = staff
        
    def get_staff(self, staff_id: str) -> Optional[StaffMember]:
        return self.staff.get(staff_id)
    
    def get_all_staff(self) -> Dict[str, StaffMember]:
        return self.staff