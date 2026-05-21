from spade import agent
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour
from spade.message import Message
from spade.template import Template
import json
import random


class TrafficLightControllerAgent(agent.Agent):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.current_state = "green"
        self.vehicle_position = None
        
    async def setup(self):
        print(f"TrafficLightControllerAgent {self.jid} started")
        
        # Add behaviours
        self.add_behaviour(self.AwaitCallBehaviour())
        self.add_behaviour(self.SendTrafficLightStateBehaviour())
        
    class AwaitCallBehaviour(CyclicBehaviour):
        async def run(self):
            # Wait for call from navigation manager to change light
            template = Template()
            template.set_metadata("ontology", "change-light")
            msg = await self.receive(template)
            if msg:
                print(f"TrafficLightController: Received light change request")
                # Change the light state
                if self.agent.current_state == "green":
                    self.agent.current_state = "red"
                else:
                    self.agent.current_state = "green"
                
                # Send updated state back to navigation manager
                response = Message(to=str(msg.sender),
                                  body=json.dumps({"trafficLightState": self.agent.current_state}),
                                  metadata={"performative": "inform", "ontology": "traffic-light-state"})
                await self.send(response)
                
    class SendTrafficLightStateBehaviour(PeriodicBehaviour):
        async def run(self):
            # Send traffic light state to navigation manager
            msg = Message(to="navigation_manager@localhost",
                         body=json.dumps({"trafficLightState": self.agent.current_state}),
                         metadata={"performative": "inform", "ontology": "traffic-light-state"})
            await self.send(msg)
            print(f"TrafficLightController: Sent traffic light state {self.agent.current_state}")
            
            # Simulate some vehicle position updates
            if self.agent.vehicle_position is None:
                self.agent.vehicle_position = "A"
            else:
                if self.agent.vehicle_position == "A":
                    self.agent.vehicle_position = "C"
                elif self.agent.vehicle_position == "C":
                    self.agent.vehicle_position = "D"
                elif self.agent.vehicle_position == "D":
                    self.agent.vehicle_position = "B"
