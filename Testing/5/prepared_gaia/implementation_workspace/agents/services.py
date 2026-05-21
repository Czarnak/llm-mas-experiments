import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
from datetime import datetime
import uuid

from core.message_types import SpecialNotification
from utils.logger import get_logger


class ServicesAgent(Agent):
    def __init__(self, jid: str, password: str):
        super().__init__(jid, password)
        self.logger = get_logger("ServicesAgent")
        
    async def setup(self):
        self.logger.info(f"Starting ServicesAgent: {self.jid}")
        
        # Add the behaviour to subscribe to special notifications
        self.add_behaviour(self.SubscribeSpecialNotificationBehaviour())
        
    class SubscribeSpecialNotificationBehaviour(CyclicBehaviour):
        async def run(self):
            # Listen for special notifications
            template = Template()
            template.subject = "SpecialNotification"
            
            msg = await self.receive(template)
            if msg:
                self.agent.logger.info(f"Received special notification: {msg.body}")
                
                # In a real system, this would process emergency notifications
                # For demonstration, we'll just log the receipt
                
                # Simulate processing the notification
                special_notification_dict = eval(msg.body)
                special_notification = SpecialNotification(
                    id=special_notification_dict["id"],
                    recipient_id=special_notification_dict["recipient_id"],
                    message=special_notification_dict["message"],
                    severity=special_notification_dict["severity"],
                    timestamp=datetime.fromisoformat(special_notification_dict["timestamp"]),
                    type=special_notification_dict["type"]
                )
                
                self.agent.logger.info(f"Processing emergency notification: {special_notification.message}")