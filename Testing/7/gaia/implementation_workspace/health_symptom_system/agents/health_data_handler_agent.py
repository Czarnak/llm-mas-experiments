from agents.base_agent import BaseAgent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import json
import pandas as pd
from datetime import datetime


class HealthDataHandlerAgent(BaseAgent):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.stored_symptoms = []
        self.logger.info(f"HealthDataHandlerAgent {self.jid} initialized")

    async def setup(self):
        await super().setup()
        self.logger.info(f"HealthDataHandlerAgent {self.jid} setup completed")

    async def store_symptoms(self, processed_symptoms):
        """Store processed symptoms"""
        try:
            # Store in memory for now (in a real system, this would be a database)
            self.stored_symptoms.append(processed_symptoms)
            self.logger.info(f"Symptoms stored: {processed_symptoms}")
            
            # Send to HealthAnalyzer
            msg = Message(to="health_analyzer@localhost", 
                          body=json.dumps(processed_symptoms), 
                          subject="AggregateHealthData")
            await self.send(msg)
            self.logger.info("Symptoms sent to HealthAnalyzer")
            return processed_symptoms
        except Exception as e:
            self.logger.error(f"Error storing symptoms: {e}")
            return None

    async def aggregate_data(self):
        """Aggregate health data for analysis"""
        try:
            # In a real system, this would involve more complex aggregation
            # For now, we'll just return the stored symptoms
            aggregated_data = {
                "symptoms": self.stored_symptoms,
                "total_count": len(self.stored_symptoms),
                "timestamp": self.get_timestamp()
            }
            
            # Send to HealthAnalyzer
            msg = Message(to="health_analyzer@localhost", 
                          body=json.dumps(aggregated_data), 
                          subject="AggregateHealthData")
            await self.send(msg)
            self.logger.info("Aggregated data sent to HealthAnalyzer")
            return aggregated_data
        except Exception as e:
            self.logger.error(f"Error aggregating data: {e}")
            return None

    def get_timestamp(self):
        return datetime.now().isoformat()

    async def handle_message(self, msg):
        """Handle incoming messages"""
        if msg.subject == "ForwardProcessedSymptoms":
            await self.store_symptoms(json.loads(msg.body))
        elif msg.subject == "AggregateHealthData":
            await self.aggregate_data()
        else:
            self.logger.warning(f"Unknown message subject: {msg.subject}")
