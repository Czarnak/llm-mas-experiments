from agents.base_agent import BaseAgent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import json


class RecommendationEngineAgent(BaseAgent):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.recommendations = []
        self.logger.info(f"RecommendationEngineAgent {self.jid} initialized")

    async def setup(self):
        await super().setup()
        self.logger.info(f"RecommendationEngineAgent {self.jid} setup completed")

    async def generate_recommendation(self, user_symptoms, health_trends, analyzed_patterns):
        """Generate personalized recommendation for user"""
        try:
            # In a real system, this would involve more sophisticated logic
            # For demonstration, we'll create simple recommendations
            recommendation = {
                "user_symptoms": user_symptoms,
                "health_trends": health_trends,
                "analyzed_patterns": analyzed_patterns,
                "recommendation": self.create_recommendation_text(user_symptoms, analyzed_patterns),
                "timestamp": self.get_timestamp(),
                "recommendation_id": str(self.agent_id)
            }
            
            self.recommendations.append(recommendation)
            self.logger.info(f"Recommendation generated: {recommendation}")
            return recommendation
        except Exception as e:
            self.logger.error(f"Error generating recommendation: {e}")
            return None

    def create_recommendation_text(self, symptoms, patterns):
        """Create recommendation text based on symptoms and patterns"""
        # Simple recommendation logic for demonstration
        if not symptoms:
            return "No symptoms detected. No specific recommendations."
        
        # Check for serious symptoms
        serious_symptoms = ["fever", "headache"]
        has_serious = any(symptom in serious_symptoms for symptom in symptoms)
        
        if has_serious:
            return "Based on your symptoms, it's recommended to consult a healthcare professional soon."
        
        # General recommendations
        return "Based on your symptoms, you may want to rest and monitor your condition. If symptoms worsen, please consult a doctor."

    def get_timestamp(self):
        from datetime import datetime
        return datetime.now().isoformat()

    async def handle_message(self, msg):
        """Handle incoming messages"""
        if msg.subject == "GenerateRecommendations":
            # This would be called from UserAgent when receiving recommendations
            pass
        else:
            self.logger.warning(f"Unknown message subject: {msg.subject}")
