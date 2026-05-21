import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour
from spade.message import Message
from spade.template import Template
from datetime import datetime
import uuid

from core.message_types import Route, MatchInformation, OptimizedRoute
from utils.logger import get_logger


class RoutePlannerAgent(Agent):
    def __init__(self, jid: str, password: str):
        super().__init__(jid, password)
        self.logger = get_logger("RoutePlannerAgent")
        
    async def setup(self):
        self.logger.info(f"Starting RoutePlannerAgent: {self.jid}")
        
        # Add the behaviour to await match information
        self.add_behaviour(self.AwaitMatchInformationBehaviour())
        
        # Add the behaviour to produce routes
        self.add_behaviour(self.ProduceRouteBehaviour())
        
    class AwaitMatchInformationBehaviour(CyclicBehaviour):
        async def run(self):
            # Listen for match information
            template = Template()
            template.subject = "MatchInformation"
            
            msg = await self.receive(template)
            if msg:
                self.agent.logger.info(f"Received match information: {msg.body}")
                
                # In a real system, this would process the match and generate route
                # For demonstration, we'll just simulate the process
                
    class ProduceRouteBehaviour(CyclicBehaviour):
        async def run(self):
            # Periodically produce routes (simulated)
            # In a real system, this would be triggered by match information
            
            route = Route(
                id=str(uuid.uuid4()),
                match_id="match_123",
                start_location="Distribution Center X",
                end_location="Hospital A",
                waypoints=["Main St", "Oak Ave", "Pine Rd"],
                estimated_time=45
            )
            
            self.agent.logger.info(f"Producing route: {route.id}")
            
            # Send route to TruckDriver
            msg = Message(
                to="truck_driver@localhost",
                body=str(route.__dict__),
                subject="Route"
            )
            await self.send(msg)
            
            # Wait for a while before producing next route
            await asyncio.sleep(35)