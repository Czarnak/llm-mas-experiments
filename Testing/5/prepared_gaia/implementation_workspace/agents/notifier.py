import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour
from spade.message import Message
from spade.template import Template
from datetime import datetime
import uuid

from core.message_types import Notification, SpecialNotification
from utils.logger import get_logger


class NotifierAgent(Agent):
    def __init__(self, jid: str, password: str):
        super().__init__(jid, password)
        self.logger = get_logger("NotifierAgent")
        
    async def setup(self):
        self.logger.info(f"Starting NotifierAgent: {self.jid}")
        
        # Add the behaviour to await cloud information
        self.add_behaviour(self.AwaitCloudInformationBehaviour())
        
        # Add the behaviour to produce notifications
        self.add_behaviour(self.ProduceNotificationBehaviour())
        
        # Add the behaviour to produce special notifications
        self.add_behaviour(self.ProduceSpecialNotificationBehaviour())
        
    class AwaitCloudInformationBehaviour(CyclicBehaviour):
        async def run(self):
            # Listen for cloud information (simulated)
            template = Template()
            template.subject = "CloudInformation"
            
            msg = await self.receive(template)
            if msg:
                self.agent.logger.info(f"Received cloud information: {msg.body}")
                
                # In a real system, this would process cloud data and generate notifications
                # For now, we'll just simulate sending a notification
                
    class ProduceNotificationBehaviour(CyclicBehaviour):
        async def run(self):
            # Periodically produce notifications
            notification = Notification(
                id=str(uuid.uuid4()),
                recipient_id="person_in_need@localhost",
                message="Your request for medicines has been matched with available supplies.",
                type="request_update"
            )
            
            self.agent.logger.info(f"Producing notification: {notification.id}")
            
            # Send notification to PersonInNeed
            msg = Message(
                to=notification.recipient_id,
                body=str(notification.__dict__),
                subject="Notification"
            )
            await self.send(msg)
            
            # Wait for a while before producing next notification
            await asyncio.sleep(30)
            
    class ProduceSpecialNotificationBehaviour(CyclicBehaviour):
        async def run(self):
            # Periodically produce special notifications
            special_notification = SpecialNotification(
                id=str(uuid.uuid4()),
                recipient_id="services@localhost",
                message="Road closure detected on Main Street due to flooding.",
                severity="high"
            )
            
            self.agent.logger.info(f"Producing special notification: {special_notification.id}")
            
            # Send special notification to Services
            msg = Message(
                to=special_notification.recipient_id,
                body=str(special_notification.__dict__),
                subject="SpecialNotification"
            )
            await self.send(msg)
            
            # Wait for a while before producing next special notification
            await asyncio.sleep(45)