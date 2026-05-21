from crewai_tools import BaseTool
from typing import List, Dict, Any
import json


class DataGeneratorTool(BaseTool):
    name: str = "Data Generator Tool"
    description: str = "Generates realistic sensor data for pet monitoring"

    def _run(self, **kwargs) -> str:
        # Import here to avoid circular imports
        from agents.sensor_agent import SensorAgent
        
        sensor_agent = SensorAgent()
        data = sensor_agent.generate_sensor_data()
        return json.dumps(data)


class DataAggregatorTool(BaseTool):
    name: str = "Data Aggregator Tool"
    description: str = "Aggregates raw sensor data from multiple sources"

    def _run(self, raw_data_list: List[Dict[str, Any]]) -> str:
        # Import here to avoid circular imports
        from agents.smart_collar_agent import SmartCollarAgent
        
        smart_collar_agent = SmartCollarAgent()
        aggregated = smart_collar_agent.aggregate_data(raw_data_list)
        return json.dumps(aggregated)


class DataParserTool(BaseTool):
    name: str = "Data Parser Tool"
    description: str = "Parses aggregated data into structured format"

    def _run(self, aggregated_data: Dict[str, Any]) -> str:
        # Import here to avoid circular imports
        from agents.smart_collar_agent import SmartCollarAgent
        
        smart_collar_agent = SmartCollarAgent()
        parsed = smart_collar_agent.parse_data(aggregated_data)
        return json.dumps(parsed)


class DataAnalyzerTool(BaseTool):
    name: str = "Data Analyzer Tool"
    description: str = "Analyzes parsed data to detect potential health issues"

    def _run(self, parsed_data: Dict[str, Any]) -> str:
        # Import here to avoid circular imports
        from agents.analyzer_agent import AnalyzerAgent
        
        analyzer_agent = AnalyzerAgent()
        analysis = analyzer_agent.analyze_data(parsed_data)
        return json.dumps(analysis)


class AppointmentPlannerTool(BaseTool):
    name: str = "Appointment Planner Tool"
    description: str = "Plans vet appointments when health concerns are detected"

    def _run(self, health_analysis: Dict[str, Any], current_appointments: List[Dict[str, Any]]) -> str:
        # Import here to avoid circular imports
        from agents.master_agent import MasterAgent
        
        master_agent = MasterAgent()
        decision = master_agent.make_decision(health_analysis, current_appointments)
        return json.dumps(decision)
