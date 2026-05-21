from agents.base_agent import BaseAgent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import json
import pandas as pd
from datetime import datetime


class HealthAnalyzerAgent(BaseAgent):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.analyzed_patterns = []
        self.logger.info(f"HealthAnalyzerAgent {self.jid} initialized")

    async def setup(self):
        await super().setup()
        self.logger.info(f"HealthAnalyzerAgent {self.jid} setup completed")

    async def analyze_patterns(self, stored_symptoms):
        """Analyze health data for patterns and trends"""
        try:
            # In a real system, this would involve complex pattern analysis
            # For demonstration, we'll create some basic patterns
            patterns = {
                "symptom_counts": self.count_symptoms(stored_symptoms),
                "trends": self.identify_trends(stored_symptoms),
                "timestamp": self.get_timestamp(),
                "analysis_id": str(self.agent_id)
            }
            
            self.analyzed_patterns.append(patterns)
            self.logger.info(f"Patterns analyzed: {patterns}")
            
            # Send to HealthInstitution
            msg = Message(to="health_institution@localhost", 
                          body=json.dumps(patterns), 
                          subject="ProvideHealthInsights")
            await self.send(msg)
            self.logger.info("Health insights sent to HealthInstitution")
            return patterns
        except Exception as e:
            self.logger.error(f"Error analyzing patterns: {e}")
            return None

    def count_symptoms(self, symptoms_data):
        """Count occurrences of each symptom"""
        symptom_counts = {}
        for symptom_data in symptoms_data:
            if "symptoms" in symptom_data:
                for symptom in symptom_data["symptoms"]:
                    symptom_counts[symptom] = symptom_counts.get(symptom, 0) + 1
        return symptom_counts

    def identify_trends(self, symptoms_data):
        """Identify basic trends"""
        # Simple trend identification for demonstration
        return {
            "total_reports": len(symptoms_data),
            "average_symptoms_per_report": sum(len(s.get("symptoms", [])) for s in symptoms_data) / max(len(symptoms_data), 1)
        }

    def get_timestamp(self):
        return datetime.now().isoformat()

    async def handle_message(self, msg):
        """Handle incoming messages"""
        if msg.subject == "AggregateHealthData":
            await self.analyze_patterns(json.loads(msg.body))
        else:
            self.logger.warning(f"Unknown message subject: {msg.subject}")
