from agents.symptom_reporter import SymptomReporterAgent, SymptomReport
from agents.health_analyzer import HealthAnalyzerAgent, HealthDataPoint
from agents.health_authority_support import HealthAuthoritySupportAgent
from agents.user_recommendation import UserRecommendationAgent
from typing import List, Dict, Any
import uuid


class HealthSystemCoordinator:
    def __init__(self):
        self.symptom_reporter = SymptomReporterAgent()
        self.health_analyzer = HealthAnalyzerAgent()
        self.health_authority_support = HealthAuthoritySupportAgent()
        self.user_recommendation = UserRecommendationAgent()
        
        # In-memory storage for demonstration purposes
        self.health_data_store = []
        self.user_profiles = {}

    def process_symptom_report(self, report: SymptomReport, user_id: str) -> Dict[str, Any]:
        """
        Process a symptom report from a user
        """
        # Process the symptom report
        processed_report = self.symptom_reporter.process_symptom_report(report)
        
        # Store in data store
        data_point = HealthDataPoint(
            timestamp=processed_report["timestamp"],
            symptoms=processed_report["symptoms"],
            severity=processed_report["severity"],
            duration=processed_report["duration"],
            user_id=user_id
        )
        
        self.health_data_store.append(data_point)
        
        # Generate recommendations
        recommendations = self.user_recommendation.generate_recommendations(
            symptoms=processed_report["symptoms"],
            severity=processed_report["severity"],
            duration=processed_report["duration"]
        )
        
        # Generate personalized advice
        advice = self.user_recommendation.generate_personalized_advice(
            user_profile=self.user_profiles.get(user_id, {}),
            recommendations=recommendations
        )
        
        return {
            "status": "success",
            "report": processed_report,
            "recommendations": recommendations,
            "advice": advice
        }

    def analyze_health_data(self) -> Dict[str, Any]:
        """
        Analyze all collected health data
        """
        analysis_result = self.health_analyzer.analyze_health_data(self.health_data_store)
        
        # Detect anomalies
        anomalies = self.health_analyzer.detect_anomalies(self.health_data_store)
        
        # Generate insights
        insights = self.health_analyzer.generate_insights(analysis_result)
        
        return {
            "analysis": analysis_result,
            "anomalies": anomalies,
            "insights": insights
        }

    def generate_authority_report(self) -> Dict[str, Any]:
        """
        Generate report for health authorities
        """
        analysis_result = self.health_analyzer.analyze_health_data(self.health_data_store)
        anomalies = self.health_analyzer.detect_anomalies(self.health_data_store)
        insights = self.health_analyzer.generate_insights(analysis_result)
        
        authority_report = self.health_authority_support.generate_authority_report(
            analysis_result, anomalies, insights
        )
        
        return {
            "authority_report": authority_report
        }

    def generate_research_insights(self) -> Dict[str, Any]:
        """
        Generate research insights for researchers
        """
        analysis_result = self.health_analyzer.analyze_health_data(self.health_data_store)
        
        research_insights = self.health_authority_support.provide_research_insights(analysis_result)
        
        return {
            "research_insights": research_insights
        }

    def get_user_recommendations(self, user_id: str) -> Dict[str, Any]:
        """
        Get personalized recommendations for a user
        """
        # For demonstration, we'll just return the latest recommendations
        return {
            "user_id": user_id,
            "recommendations": "Based on your previous reports, we recommend continuing to monitor your symptoms and consulting a healthcare professional if they persist."
        }
