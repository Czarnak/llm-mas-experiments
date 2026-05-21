from spade import agent
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour
from spade.message import Message
from spade.template import Template
import json
import random


class RoadConditionReporterAgent(agent.Agent):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.events = [
            "accident",
            "traffic_jam",
            "road_construction",
            "weather_delay",
            "no_event"
        ]
        
    async def setup(self):
        print(f"RoadConditionReporterAgent {self.jid} started")
        
        # Add behaviours
        self.add_behaviour(self.SendRoadConditionBehaviour())
        
    class SendRoadConditionBehaviour(PeriodicBehaviour):
        async def run(self):
            # Generate random road condition
            condition = random.choice(self.agent.events)
            
            # Send road condition to navigation manager
            msg = Message(to="navigation_manager@localhost",
                         body=json.dumps({"roadCondition": condition}),
                         metadata={"performative": "inform", "ontology": "road-condition"})
            await self.send(msg)
            print(f"RoadConditionReporter: Sent road condition {condition}")
            
            # Wait for a while before sending next condition
            await asyncio.sleep(5)
