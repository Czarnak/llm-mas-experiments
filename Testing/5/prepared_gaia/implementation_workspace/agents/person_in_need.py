import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
from datetime import datetime
import uuid

from core.message_types import Request
from utils.logger import get_logger


class PersonInNeedAgent(Agent):
    def __init__(self, jid: str, password: str, db_path: str = "crisis_transport.db"):
        super().__init__(jid, password)
        self.db_path = db_path
        self.logger = get_logger("PersonInNeedAgent")
        
    async def setup(self):
        self.logger.info(f"Starting PersonInNeedAgent: {self.jid}")
        
        # Add the behaviour to produce requests
        self.add_behaviour(self.ProduceRequestBehaviour())
        
        # Add the behaviour to subscribe to truck driver location
        self.add_behaviour(self.SubscribeTruckDriverLocationBehaviour())
        
        # Add the behaviour to subscribe to notifications
        self.add_behaviour(self.SubscribeNotificationBehaviour())
        
    class ProduceRequestBehaviour(CyclicBehaviour):
        async def run(self):
            # Simulate producing a request
            request = Request(
                id=str(uuid.uuid4()),
                requester_id=str(self.agent.jid),
                resource_type="medicines",
                quantity=10,
                location="Hospital A"
            )
            
            self.agent.logger.info(f"Producing request: {request.id}")
            
            # Send request to DataHandlerAgent
            msg = Message(
                to="data_handler@localhost",
                body=str(request.__dict__),
                subject="Request"
            )
            await self.send(msg)
            
            # Wait for a while before producing next request
            await asyncio.sleep(10)
            
    class SubscribeTruckDriverLocationBehaviour(CyclicBehaviour):
        async def run(self):
            # Listen for truck driver location updates
            template = Template()
            template.sender = "truck_driver@localhost"
            template.subject = "TruckDriverLocation"
            
            msg = await self.receive(template)
            if msg:
                self.agent.logger.info(f"Received truck driver location update: {msg.body}")
                
    class SubscribeNotificationBehaviour(CyclicBehaviour):
        async def run(self):
            # Listen for notifications
            template = Template()
            template.sender = "notifier@localhost"
            template.subject = "Notification"
            
            msg = await self.receive(template)
            if msg:
                self.agent.logger.info(f"Received notification: {msg.body}")