from crewai import Agent
from pydantic import BaseModel
from typing import List, Dict, Any


class HealthAuthorityReport(BaseModel):
    report_type: str  # "epidemic", "outbreak", "trend_analysis"
    data: Dict[str, Any]
    timestamp: str
    

class HealthAuthoritySupportAgent(Agent):
    def __init__(self):
        super().__init__(
            role="Health Authority Support",
            goal="Provide health authorities and researchers with relevant data and insights",
            backstory="You are a specialized agent that supports health authorities and researchers by providing them with structured health data, trends, and insights. You help them make informed decisions about public health interventions.",
            verbose=True,
            allow_delegation=False,
            tools=[],
        )

    def generate_authority_report(self, analysis_result: Dict[str, Any], anomalies: List[Dict[str, Any]], insights: List[str]) -> HealthAuthorityReport:
        report_data = {
            "summary": {
                "total_reports": analysis_result.get("total_reports", 0),
                "symptom_distribution": analysis_result.get("symptom_distribution", {}),
                "severity_distribution": analysis_result.get("severity_distribution", {}),
            },
            "anomalies": anomalies,
            "insights": insights,
            "timestamp": "2023-01-01T00:00:00Z"
        }
        
        return HealthAuthorityReport(
            report_type="trend_analysis",
            data=report_data,
            timestamp="2023-01-01T00:00:00Z"
        )

    def generate_epidemic_report(self, data_points: List[Dict[str, Any]]) -> HealthAuthorityReport:
        # Generate an epidemic report
        report_data = {
            "type": "epidemic",
            "data_points": data_points,
            "summary": "Epidemic monitoring data",
            "timestamp": "2023-01-01T00:00:00Z"
        }
        
        return HealthAuthorityReport(
            report_type="epidemic",
            data=report_data,
            timestamp="2023-01-01T00:00:00Z"
        )

    def provide_research_insights(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        # Generate research insights
        insights = {
            "data_quality": "High quality health data",
            "trend_patterns": "Identified common patterns in symptom reporting",
            "research_opportunities": [
                "Further investigation of symptom combinations",
                "Study on seasonal variations in symptoms"
            ],
            "recommendations": [
                "Continue monitoring reported symptoms",
                "Consider additional data sources"
            ]
        }
        
        return insights