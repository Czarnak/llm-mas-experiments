import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour
from spade.message import Message
from spade.template import Template
from datetime import datetime
import uuid

from core.message_types import TruckDriverLocation, Route, OptimizedRoute
from utils.logger import get_logger


class TruckDriverAgent(Agent):
    def __init__(self, jid: str, password: str):
        super().__init__(jid, password)
        self.logger = get_logger("TruckDriverAgent")
        
    async def setup(self):
        self.logger.info(f"Starting TruckDriverAgent: {self.jid}")
        
        # Add the behaviour to produce truck driver location
        self.add_behaviour(self.ProduceTruckDriverLocationBehaviour())
        
        # Add the behaviour to subscribe to optimized route
        self.add_behaviour(self.SubscribeOptimizedRouteBehaviour())
        
    class ProduceTruckDriverLocationBehaviour(CyclicBehaviour):
        async def run(self):
            # Periodically produce truck driver location (simulated)
            location = TruckDriverLocation(
                id=str(uuid.uuid4()),
                driver_id=str(self.agent.jid),
                current_location="On route to Hospital A"
            )
            
            self.agent.logger.info(f"Producing truck driver location: {location.id}")
            
            # Send location to RouteOptimizer
            msg = Message(
                to="route_optimizer@localhost",
                body=str(location.__dict__),
                subject="TruckDriverLocation"
            )
            await self.send(msg)
            
            # Wait for a while before producing next location
            await asyncio.sleep(15)
            
    class SubscribeOptimizedRouteBehaviour(CyclicBehaviour):
        async def run(self):
            # Listen for optimized route
            template = Template()
            template.subject = "OptimizedRoute"
            
            msg = await self.receive(template)
            if msg:
                self.agent.logger.info(f"Received optimized route: {msg.body}")
                
                # In a real system, this would process the route and start delivery
                # For demonstration, we'll just log the receipt
