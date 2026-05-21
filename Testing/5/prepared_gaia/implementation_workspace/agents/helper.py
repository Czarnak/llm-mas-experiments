import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
from datetime import datetime
import uuid

from core.message_types import AvailableMaterials
from utils.logger import get_logger


class HelperAgent(Agent):
    def __init__(self, jid: str, password: str, db_path: str = "crisis_transport.db"):
        super().__init__(jid, password)
        self.db_path = db_path
        self.logger = get_logger("HelperAgent")
        
    async def setup(self):
        self.logger.info(f"Starting HelperAgent: {self.jid}")
        
        # Add the behaviour to produce requests
        self.add_behaviour(self.ProduceRequestBehaviour())
        
        # Add the behaviour to subscribe to notifications
        self.add_behaviour(self.SubscribeNotificationBehaviour())
        
    class ProduceRequestBehaviour(CyclicBehaviour):
        async def run(self):
            # Simulate producing an offer to provide materials
            materials = AvailableMaterials(
                id=str(uuid.uuid4()),
                provider_id=str(self.agent.jid),
                resource_type="medicines",
                quantity=15,
                location="Warehouse B"
            )
            
            self.agent.logger.info(f"Producing available materials: {materials.id}")
            
            # Send materials to DataHandlerAgent
            msg = Message(
                to="data_handler@localhost",
                body=str(materials.__dict__),
                subject="AvailableMaterials"
            )
            await self.send(msg)
            
            # Wait for a while before producing next offer
            await asyncio.sleep(15)
            
    class SubscribeNotificationBehaviour(CyclicBehaviour):
        async def run(self):
            # Listen for notifications
            template = Template()
            template.sender = "notifier@localhost"
            template.subject = "Notification"
            
            msg = await self.receive(template)
            if msg:
                self.agent.logger.info(f"Received notification: {msg.body}")