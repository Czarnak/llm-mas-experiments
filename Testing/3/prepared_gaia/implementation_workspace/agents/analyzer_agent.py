from crewai import Agent
from pydantic import BaseModel
from typing import List, Dict, Any


class AnalyzerAgent:
    def __init__(self):
        self.role = "Data Analyzer (LLM)"
        self.goal = "Analyze parsed data to provide useful health information"
        self.backstory = "You are a data analyzer that uses LLM capabilities to analyze pet health data and provide actionable insights."
        self.tools = []

    def create_agent(self):
        return Agent(
            role=self.role,
            goal=self.goal,
            backstory=self.backstory,
            tools=self.tools,
            verbose=True,
            allow_delegation=False
        )

    def analyze_data(self, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze parsed data to detect potential health issues"""
        # In a real implementation, this would use an LLM
        # For this simulation, we'll use simple rules-based analysis
        
        analysis = {
            "timestamp": parsed_data["timestamp"],
            "health_status": "normal",
            "recommendations": [],
            "alerts": [],
            "metrics": parsed_data["metrics"]
        }
        
        # Check for abnormal readings
        if parsed_data["metrics"]["temperature"] > 39.5:
            analysis["health_status"] = "concern"
            analysis["alerts"].append("High body temperature detected")
            analysis["recommendations"].append("Monitor temperature closely and consult vet if it persists")
        
        if parsed_data["metrics"]["heart_rate"] > 100:
            analysis["health_status"] = "concern"
            analysis["alerts"].append("Elevated heart rate detected")
            analysis["recommendations"].append("Check for signs of stress or illness")
        
        if parsed_data["metrics"]["activity_level"] < 20:
            analysis["health_status"] = "concern"
            analysis["alerts"].append("Low activity level detected")
            analysis["recommendations"].append("Encourage movement and monitor for changes")
        
        if parsed_data["metrics"]["sleep_duration"] > 10:
            analysis["health_status"] = "concern"
            analysis["alerts"].append("Excessive sleep detected")
            analysis["recommendations"].append("Monitor for signs of illness or fatigue")
        
        if not analysis["alerts"]:
            analysis["alerts"].append("No immediate health concerns detected")
            
        return analysis
