import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
import json
import uuid
from datetime import datetime


class BaseAgent(Agent):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.agent_id = str(uuid.uuid4())
        self.logger = self.get_logger()
        self.logger.info(f"BaseAgent {self.jid} initialized")

    async def setup(self):
        await super().setup()
        self.logger.info(f"BaseAgent {self.jid} setup completed")

    def get_agent_info(self):
        return {
            "agent_id": self.agent_id,
            "jid": str(self.jid),
            "type": self.__class__.__name__
        }

    def log_message(self, message, direction="received"):
        self.logger.info(f"{direction.upper()}: {message.body}")

    async def send_message(self, to, body, subject="", sender=None):
        msg = Message(to=to, body=body, subject=subject)
        if sender:
            msg.sender = sender
        await self.send(msg)
        self.logger.info(f"Message sent to {to}: {body}")

    async def receive_message(self, template=None):
        if template:
            msg = await self.wait(template)
        else:
            msg = await self.wait()
        return msg

    def create_message(self, to, body, subject=""):
        msg = Message(to=to, body=body, subject=subject)
        return msg