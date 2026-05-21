from typing import Dict, Any, Optional
from .base_agent import BaseAgent, AgentMessage
from ..models.animal import Animal
from ..models.staff import StaffMember


class AnimalRegistryAgent(BaseAgent):
    def __init__(self, agent_id: str, name: str):
        super().__init__(agent_id, name)
        self.animals: Dict[str, Animal] = {}
        self.staff: Dict[str, StaffMember] = {}
        
    def process_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        if message.protocol == "RegisterAnimal":
            return self._register_animal(message)
        elif message.protocol == "UpdateAnimalStatus":
            return self._update_animal_status(message)
        elif message.protocol == "RegisterStaffMember":
            return self._register_staff_member(message)
        else:
            # Handle unknown protocols
            return None
    
    def _register_animal(self, message: AgentMessage) -> Optional[AgentMessage]:
        animal_profile = message.content.get("AnimalProfile")
        if not animal_profile:
            return None
        
        # Create animal instance
        animal = Animal(
            id=animal_profile["id"],
            name=animal_profile["name"],
            species=animal_profile["species"],
            breed=animal_profile["breed"],
            age=animal_profile["age"],
            gender=animal_profile["gender"]
        )
        
        # Store animal
        self.animals[animal.id] = animal
        
        # Return success confirmation
        return AgentMessage(
            sender=self.agent_id,
            receiver=message.sender,
            protocol="SuccessConfirmation",
            content={"AnimalID": animal.id},
            timestamp=0.0
        )
    
    def _update_animal_status(self, message: AgentMessage) -> Optional[AgentMessage]:
        animal_id = message.content.get("AnimalID")
        status_update = message.content.get("StatusUpdate")
        
        if not animal_id or not status_update:
            return None
        
        animal = self.animals.get(animal_id)
        if not animal:
            return None
        
        # Update animal status
        animal.update_status(status_update)
        
        # Return success confirmation
        return AgentMessage(
            sender=self.agent_id,
            receiver=message.sender,
            protocol="SuccessConfirmation",
            content={"Success": True},
            timestamp=0.0
        )
    
    def _register_staff_member(self, message: AgentMessage) -> Optional[AgentMessage]:
        staff_profile = message.content.get("StaffProfile")
        if not staff_profile:
            return None
        
        # Create staff member instance
        staff = StaffMember(
            id=staff_profile["id"],
            name=staff_profile["name"],
            role=staff_profile["role"],
            skills=staff_profile.get("skills", []),
            preferences=staff_profile.get("preferences", {})
        )
        
        # Store staff member
        self.staff[staff.id] = staff
        
        # Return staff ID
        return AgentMessage(
            sender=self.agent_id,
            receiver=message.sender,
            protocol="StaffID",
            content={"StaffID": staff.id},
            timestamp=0.0
        )
    
    def get_capabilities(self) -> Dict[str, Any]:
        return {
            "roles": ["AnimalRegistry"],
            "protocols": ["RegisterAnimal", "UpdateAnimalStatus", "RegisterStaffMember"],
            "permissions": {
                "read": ["AnimalProfile", "AnimalID", "StaffProfile", "StaffID"],
                "write": ["AnimalProfile", "AnimalID", "StaffProfile", "StaffID"],
                "consume": ["AnimalProfile", "StatusUpdate", "StaffProfile"],
                "produce": ["AnimalID", "StaffID", "SuccessConfirmation"]
            }
        }
    
    def get_animal(self, animal_id: str) -> Optional[Animal]:
        return self.animals.get(animal_id)
    
    def get_staff(self, staff_id: str) -> Optional[StaffMember]:
        return self.staff.get(staff_id)
    
    def get_all_animals(self) -> Dict[str, Animal]:
        return self.animals
    
    def get_all_staff(self) -> Dict[str, StaffMember]:
        return self.staff