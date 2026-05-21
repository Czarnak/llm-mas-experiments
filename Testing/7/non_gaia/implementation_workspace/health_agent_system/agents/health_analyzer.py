from crewai import Agent
from pydantic import BaseModel
from typing import List, Dict, Any
import json


class HealthDataPoint(BaseModel):
    timestamp: str
    symptoms: List[str]
    severity: str
    duration: str
    user_id: str
    

class HealthAnalyzerAgent(Agent):
    def __init__(self):
        super().__init__(
            role="Health Data Analyzer",
            goal="Analyze health data patterns and provide insights in real-time",
            backstory="You are a sophisticated health data analysis agent that processes user health reports to identify patterns, trends, and potential health risks. You provide real-time analysis and insights to support both users and health authorities.",
            verbose=True,
            allow_delegation=False,
            tools=[],
        )

    def analyze_health_data(self, data_points: List[HealthDataPoint]):
        # Simple pattern analysis for demonstration
        analysis_result = {
            "total_reports": len(data_points),
            "symptom_distribution": {},
            "severity_distribution": {},
            "trend_analysis": "No significant trends detected"
        }
        
        # Count symptoms
        for data_point in data_points:
            for symptom in data_point.symptoms:
                if symptom not in analysis_result["symptom_distribution"]:
                    analysis_result["symptom_distribution"][symptom] = 0
                analysis_result["symptom_distribution"][symptom] += 1
                
            if data_point.severity not in analysis_result["severity_distribution"]:
                analysis_result["severity_distribution"][data_point.severity] = 0
            analysis_result["severity_distribution"][data_point.severity] += 1
            
        return analysis_result

    def detect_anomalies(self, data_points: List[HealthDataPoint]):
        # Simple anomaly detection logic
        anomalies = []
        
        # Check for unusual symptom combinations
        if len(data_points) > 5:
            symptom_combinations = {}
            for data_point in data_points:
                combo = tuple(sorted(data_point.symptoms))
                if combo not in symptom_combinations:
                    symptom_combinations[combo] = 0
                symptom_combinations[combo] += 1
                
                # Flag combinations that appear frequently
                if symptom_combinations[combo] > 2:
                    anomalies.append({
                        "type": "symptom_combination",
                        "combination": list(combo),
                        "frequency": symptom_combinations[combo]
                    })
        
        return anomalies

    def generate_insights(self, analysis_result: Dict[str, Any]):
        insights = []
        
        # Generate insights based on analysis
        if analysis_result["symptom_distribution"]:
            most_common = max(analysis_result["symptom_distribution"].items(), key=lambda x: x[1])
            insights.append(f"Most common symptom reported: {most_common[0]} ({most_common[1]} reports)")
            
        if analysis_result["severity_distribution"]:
            most_severe = max(analysis_result["severity_distribution"].items(), key=lambda x: x[1])
            insights.append(f"Most common severity level: {most_severe[0]} ({most_severe[1]} reports)")
            
        return insights