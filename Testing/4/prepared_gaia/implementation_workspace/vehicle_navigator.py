from spade import agent
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour
from spade.message import Message
from spade.template import Template
import json
import random


class VehicleNavigatorAgent(agent.Agent):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.current_position = "A"
        self.preferred_route = None
        self.route = None
        
    async def setup(self):
        print(f"VehicleNavigatorAgent {self.jid} started")
        
        # Add behaviours
        self.add_behaviour(self.SendPositionBehaviour())
        self.add_behaviour(self.RequestRouteBehaviour())
        
    class SendPositionBehaviour(PeriodicBehaviour):
        async def run(self):
            # Send position to navigation manager
            msg = Message(to="navigation_manager@localhost",
                         body=json.dumps({"vehiclePosition": self.agent.current_position}),
                         metadata={"performative": "inform", "ontology": "vehicle-position"})
            await self.send(msg)
            print(f"VehicleNavigator: Sent position {self.agent.current_position}")
            
            # Update position for next cycle
            if self.agent.current_position == "A":
                self.agent.current_position = "C"
            elif self.agent.current_position == "C":
                self.agent.current_position = "D"
            elif self.agent.current_position == "D":
                self.agent.current_position = "B"
            
    class RequestRouteBehaviour(CyclicBehaviour):
        async def run(self):
            # Request route from navigation manager
            msg = Message(to="navigation_manager@localhost",
                         body=json.dumps({}),
                         metadata={"performative": "request", "ontology": "route-request"})
            await self.send(msg)
            print("VehicleNavigator: Requested route")
            
            # Wait for response
            template = Template()
            template.set_metadata("ontology", "route-response")
            response = await self.receive(template)
            if response:
                data = json.loads(response.body)
                self.agent.route = data["route"]
                print(f"VehicleNavigator: Received route: {self.agent.route}")