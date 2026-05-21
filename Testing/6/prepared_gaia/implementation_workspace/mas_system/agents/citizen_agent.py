from .base_agent import BaseAgent
from mas_system.protocols.service_demand_protocol import ServiceDemandProtocol
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from typing import Dict, Any


class CitizenBehaviour(CyclicBehaviour):
    """
    Behaviour for Citizen agent
    """
    
    async def run(self):
        # This is a simplified version - in a real system, this would handle
        # receiving messages and responding appropriately
        msg = await self.receive(timeout=10)
        if msg:
            print(f"Citizen received: {msg.body}")
            # Process the message
            protocol = self.agent.get_protocol("ServiceDemandRequest")
            if protocol:
                result = protocol.process_message(eval(msg.body))
                if result:
                    # Send response
                    response = Message(to=msg.sender, body=str(result))
                    response.set_metadata("protocol", "ServiceDemandRequest")
                    await self.send(response)


class CitizenAgent(BaseAgent):
    """
    Agent representing a citizen reporting service demands
    """
    
    def __init__(self, jid: str, password: str, agent_name: str):
        super().__init__(jid, password, agent_name)
        self.citizen_id = None
        self.location = None
        
    async def setup(self):
        await super().setup()
        
        # Add protocols
        service_protocol = ServiceDemandProtocol()
        self.add_protocol("ServiceDemandRequest", service_protocol)
        
        # Add behaviours
        behaviour = CitizenBehaviour()
        self.add_behaviour(behaviour)
        
    def set_citizen_details(self, citizen_id: str, location: str):
        """
        Set the details of the citizen
        """
        self.citizen_id = citizen_id
        self.location = location
        
    def report_service_demand(self, service_type: str, priority: str = "medium") -> Dict[str, Any]:
        """
        Report a service demand
        """
        protocol = self.get_protocol("ServiceDemandRequest")
        if protocol:
            return protocol.create_demand_message(
                self.citizen_id,
                service_type,
                self.location,
                priority
            )
        return {}
        
    def withdraw_demand(self):
        """
        Withdraw a service demand
        """
        print(f"{self.agent_name} withdrawing service demand")
        # In a real implementation, this would send a withdrawal message
        return True