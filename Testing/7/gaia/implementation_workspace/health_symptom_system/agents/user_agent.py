from agents.base_agent import BaseAgent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import json


class UserAgent(BaseAgent):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.symptoms = []
        self.recommendations = []
        self.logger.info(f"UserAgent {self.jid} initialized")

    async def setup(self):
        await super().setup()
        self.logger.info(f"UserAgent {self.jid} setup completed")

    async def submit_symptoms(self, symptoms_text):
        """Submit symptoms to LLMProcessor"""
        # Create message to LLMProcessor
        msg = Message(to="llm_processor@localhost", body=symptoms_text, subject="SubmitSymptoms")
        await self.send(msg)
        self.logger.info(f"Symptoms submitted: {symptoms_text}")
        return msg

    async def receive_recommendation(self, recommendation):
        """Receive personalized recommendation"""
        self.recommendations.append(recommendation)
        self.logger.info(f"Recommendation received: {recommendation}")
        return recommendation