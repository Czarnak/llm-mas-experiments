from agents.base_agent import BaseAgent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import json
import openai


class LLMProcessorAgent(BaseAgent):
    def __init__(self, jid, password, openai_api_key):
        super().__init__(jid, password)
        self.openai_api_key = openai_api_key
        self.logger.info(f"LLMProcessorAgent {self.jid} initialized")

    async def setup(self):
        await super().setup()
        self.logger.info(f"LLMProcessorAgent {self.jid} setup completed")

    async def process_symptoms(self, user_input):
        """Process user symptoms using LLM"""
        try:
            # For this implementation, we'll simulate the LLM processing
            # In a real implementation, we would call OpenAI API
            processed_symptoms = {
                "user_input": user_input,
                "processed": True,
                "symptoms": self.extract_symptoms(user_input),
                "timestamp": self.get_timestamp(),
                "user_id": self.agent_id
            }
            
            # Create message to HealthDataHandler
            msg = Message(to="health_data_handler@localhost", 
                          body=json.dumps(processed_symptoms), 
                          subject="ForwardProcessedSymptoms")
            await self.send(msg)
            self.logger.info(f"Processed symptoms sent to HealthDataHandler: {processed_symptoms}")
            return processed_symptoms
        except Exception as e:
            self.logger.error(f"Error processing symptoms: {e}")
            return None

    def extract_symptoms(self, text):
        """Extract symptoms from natural language input"""
        # This is a simplified implementation
        # In a real system, this would be more sophisticated
        symptoms = []
        # Simple keyword matching for demonstration
        keywords = ["fever", "cough", "headache", "fatigue", "nausea", "vomiting", "diarrhea"]
        for keyword in keywords:
            if keyword.lower() in text.lower():
                symptoms.append(keyword)
        return symptoms

    def get_timestamp(self):
        from datetime import datetime
        return datetime.now().isoformat()

    async def handle_message(self, msg):
        """Handle incoming messages"""
        if msg.subject == "SubmitSymptoms":
            await self.process_symptoms(msg.body)
        else:
            self.logger.warning(f"Unknown message subject: {msg.subject}")
