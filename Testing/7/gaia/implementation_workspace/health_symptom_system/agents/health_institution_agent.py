from agents.base_agent import BaseAgent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import json


class HealthInstitutionAgent(BaseAgent):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.health_insights = []
        self.logger.info(f"HealthInstitutionAgent {self.jid} initialized")

    async def setup(self):
        await super().setup()
        self.logger.info(f"HealthInstitutionAgent {self.jid} setup completed")

    async def receive_insights(self, insights):
        """Receive health insights from analyzer"""
        try:
            self.health_insights.append(insights)
            self.logger.info(f"Health insights received: {insights}")
            return insights
        except Exception as e:
            self.logger.error(f"Error receiving insights: {e}")
            return None

    async def handle_message(self, msg):
        """Handle incoming messages"""
        if msg.subject == "ProvideHealthInsights":
            await self.receive_insights(json.loads(msg.body))
        else:
            self.logger.warning(f"Unknown message subject: {msg.subject}")
