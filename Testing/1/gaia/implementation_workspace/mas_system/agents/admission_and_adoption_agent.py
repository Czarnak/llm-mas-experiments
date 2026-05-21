from typing import Dict, Any, Optional
from .base_agent import BaseAgent, AgentMessage
from ..models.animal import Animal


class AdmissionAndAdoptionAgent(BaseAgent):
    def __init__(self, agent_id: str, name: str):
        super().__init__(agent_id, name)
        self.animals: Dict[str, Animal] = {}
        
    def process_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        if message.protocol == "ProcessAnimalAdmission":
            return self._process_animal_admission(message)
        elif message.protocol == "ManageAdoption":
            return self._manage_adoption(message)
        else:
            # Handle unknown protocols
            return None
    
    def _process_animal_admission(self, message: AgentMessage) -> Optional[AgentMessage]:
        admission_data = message.content.get("AdmissionData")
        if not admission_data:
            return None
        
        # Create animal instance from admission data
        animal = Animal(
            id=admission_data["id"],
            name=admission_data["name"],
            species=admission_data["species"],
            breed=admission_data["breed"],
            age=admission_data["age"],
            gender=admission_data["gender"],
            health_status=admission_data.get("health_status", "healthy"),
            adoption_status=admission_data.get("adoption_status", "pending")
        )
        
        # Store animal
        self.animals[animal.id] = animal
        
        # Return admission confirmation
        return AgentMessage(
            sender=self.agent_id,
            receiver=message.sender,
            protocol="AdmissionConfirmation",
            content={"Success": True},
            timestamp=0.0
        )
    
    def _manage_adoption(self, message: AgentMessage) -> Optional[AgentMessage]:
        adoption_request = message.content.get("AdoptionRequest")
        if not adoption_request:
            return None
        
        # In a real implementation, this would process adoption requests
        # For now, we'll just return a confirmation
        return AgentMessage(
            sender=self.agent_id,
            receiver=message.sender,
            protocol="AdoptionStatusUpdate",
            content={"Status": "processed"},
            timestamp=0.0
        )
    
    def get_capabilities(self) -> Dict[str, Any]:
        return {
            "roles": ["AnimalAdmissionProcess", "AdoptionProcess"],
            "protocols": ["ProcessAnimalAdmission", "ManageAdoption"],
            "permissions": {
                "read": ["AdmissionData", "AdoptionRequest"],
                "write": ["AdmissionData", "AdoptionRequest"],
                "consume": ["AdmissionData", "AdoptionRequest"],
                "produce": ["AdmissionConfirmation", "AdoptionStatusUpdate"]
            }
        }
    
    def get_animal(self, animal_id: str) -> Optional[Animal]:
        return self.animals.get(animal_id)
    
    def get_all_animals(self) -> Dict[str, Animal]:
        return self.animals