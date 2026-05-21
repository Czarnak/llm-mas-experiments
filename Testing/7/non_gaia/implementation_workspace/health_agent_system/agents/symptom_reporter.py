from crewai import Agent
from pydantic import BaseModel
from typing import List, Optional


class SymptomReport(BaseModel):
    symptoms: List[str]
    severity: str  # mild, moderate, severe
    duration: str  # hours, days, weeks
    additional_notes: Optional[str] = None


class SymptomReporterAgent(Agent):
    def __init__(self):
        super().__init__(
            role="Symptom Reporter",
            goal="Collect and analyze user-reported symptoms in a structured format",
            backstory="You are a specialized agent designed to help users report their symptoms in a clear, structured way. You guide users through the process of describing their symptoms accurately and provide recommendations based on their reports.",
            verbose=True,
            allow_delegation=False,
            tools=[],
        )

    def process_symptom_report(self, report: SymptomReport):
        # Process the symptom report
        return {
            "status": "processed",
            "symptoms": report.symptoms,
            "severity": report.severity,
            "duration": report.duration,
            "notes": report.additional_notes,
            "timestamp": "2023-01-01T00:00:00Z"
        }

    def generate_recommendations(self, report: SymptomReport):
        # Generate recommendations based on symptoms
        recommendations = []
        
        # Simple logic for demonstration
        if "fever" in report.symptoms:
            recommendations.append("Monitor your temperature and stay hydrated")
        if "headache" in report.symptoms:
            recommendations.append("Rest in a quiet, dark room")
        if "cough" in report.symptoms:
            recommendations.append("Use a humidifier and consider over-the-counter cough syrup")
        
        return recommendations
