from crewai import Agent
from pydantic import BaseModel
from typing import List, Dict, Any


class Recommendation(BaseModel):
    type: str  # "medical_advice", "self_care", "when_to_seek_help"
    content: str
    priority: str  # "low", "medium", "high"
    

class UserRecommendationAgent(Agent):
    def __init__(self):
        super().__init__(
            role="User Recommendation Engine",
            goal="Provide personalized health recommendations to users based on their symptoms and health data",
            backstory="You are a health recommendation agent that helps users understand their symptoms and provides appropriate guidance. You can recommend self-care measures, when to seek medical help, or direct them to appropriate medical resources.",
            verbose=True,
            allow_delegation=False,
            tools=[],
        )

    def generate_recommendations(self, symptoms: List[str], severity: str, duration: str) -> List[Recommendation]:
        recommendations = []
        
        # Generate recommendations based on symptoms and severity
        if "fever" in symptoms:
            recommendations.append(Recommendation(
                type="self_care",
                content="Monitor your temperature and stay hydrated. Rest in a comfortable environment.",
                priority="medium"
            ))
            
        if "headache" in symptoms:
            recommendations.append(Recommendation(
                type="self_care",
                content="Rest in a quiet, dark room. Apply a cold compress to your forehead if needed.",
                priority="low"
            ))
            
        if "cough" in symptoms:
            recommendations.append(Recommendation(
                type="self_care",
                content="Use a humidifier and consider over-the-counter cough syrup. Stay hydrated.",
                priority="medium"
            ))
            
        if "chest pain" in symptoms or "difficulty breathing" in symptoms:
            recommendations.append(Recommendation(
                type="when_to_seek_help",
                content="Seek immediate medical attention. These symptoms can be serious.",
                priority="high"
            ))
            
        if severity == "severe" or "severe" in symptoms:
            recommendations.append(Recommendation(
                type="when_to_seek_help",
                content="Consult a healthcare professional immediately due to severe symptoms.",
                priority="high"
            ))
            
        if duration == "days" or duration == "weeks":
            recommendations.append(Recommendation(
                type="when_to_seek_help",
                content="Consider consulting a healthcare professional if symptoms persist.",
                priority="medium"
            ))
            
        # Add a general recommendation
        recommendations.append(Recommendation(
            type="medical_advice",
            content="Always consult with a healthcare professional for proper diagnosis and treatment.",
            priority="medium"
        ))
        
        return recommendations

    def generate_personalized_advice(self, user_profile: Dict[str, Any], recommendations: List[Recommendation]) -> str:
        # Generate personalized advice based on user profile
        advice = "Based on your reported symptoms, here's what we recommend:"
        
        for rec in recommendations:
            advice += f"\n- {rec.content} ({rec.priority} priority)"
            
        advice += "\n\nPlease note that this is general advice and not a substitute for professional medical consultation."
        
        return advice
