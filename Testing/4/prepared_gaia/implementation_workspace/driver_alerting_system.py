from spade import agent
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour
from spade.message import Message
from spade.template import Template
import json
import random


class DriverAlertingSystemAgent(agent.Agent):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.alerts = []
        
    async def setup(self):
        print(f"DriverAlertingSystemAgent {self.jid} started")
        
        # Add behaviours
        self.add_behaviour(self.RequestRouteBehaviour())
        
    class RequestRouteBehaviour(CyclicBehaviour):
        async def run(self):
            # Request route from navigation manager
            msg = Message(to="navigation_manager@localhost",
                         body=json.dumps({}),
                         metadata={"performative": "request", "ontology": "route-request"})
            await self.send(msg)
            print("DriverAlertingSystem: Requested route")
            
            # Wait for response
            template = Template()
            template.set_metadata("ontology", "route-response")
            response = await self.receive(template)
            if response:
                data = json.loads(response.body)
                route = data["route"]
                print(f"DriverAlertingSystem: Received route for alerting: {route}")
                
                # Generate alert based on route
                alert = {
                    "message": f"Vehicle approaching with route: {route['waypoints']}",
                    "time": route["estimated_time"],
                    "conditions": route["conditions"]
                }
                self.agent.alerts.append(alert)
                print(f"DriverAlertingSystem: Generated alert: {alert}")
