from typing import List, Dict, Any
import json

class DataGeneratorTool:
    def __init__(self):
        self.name = "Data Generator Tool"
        self.description = "Generates realistic sensor data for pet monitoring"

    def run(self, **kwargs) -> str:
        # Import here to avoid circular imports
        from agents.sensor_agent import SensorAgent
        
        sensor_agent = SensorAgent()
        data = sensor_agent.generate_sensor_data()
        return json.dumps(data)

class DataAggregatorTool:
    def __init__(self):
        self.name = "Data Aggregator Tool"
        self.description = "Aggregates raw sensor data from multiple sources"

    def run(self, raw_data_list: List[Dict[str, Any]]) -> str:
        # Import here to avoid circular imports
        from agents.smart_collar_agent import SmartCollarAgent
        
        smart_collar_agent = SmartCollarAgent()
        aggregated = smart_collar_agent.aggregate_data(raw_data_list)
        return json.dumps(aggregated)

class DataParserTool:
    def __init__(self):
        self.name = "Data Parser Tool"
        self.description = "Parses aggregated data into structured format"

    def run(self, aggregated_data: Dict[str, Any]) -> str:
        # Import here to avoid circular imports
        from agents.smart_collar_agent import SmartCollarAgent
        
        smart_collar_agent = SmartCollarAgent()
        parsed = smart_collar_agent.parse_data(aggregated_data)
        return json.dumps(parsed)

class DataAnalyzerTool:
    def __init__(self):
        self.name = "Data Analyzer Tool"
        self.description = "Analyzes parsed data to detect potential health issues"

    def run(self, parsed_data: Dict[str, Any]) -> str:
        # Import here to avoid circular imports
        from agents.analyzer_agent import AnalyzerAgent
        
        analyzer_agent = AnalyzerAgent()
        analysis = analyzer_agent.analyze_data(parsed_data)
        return json.dumps(analysis)

class AppointmentPlannerTool:
    def __init__(self):
        self.name = "Appointment Planner Tool"
        self.description = "Plans vet appointments when health concerns are detected"

    def run(self, health_analysis: Dict[str, Any], current_appointments: List[Dict[str, Any]]) -> str:
        # Import here to avoid circular imports
        from agents.master_agent import MasterAgent
        
        master_agent = MasterAgent()
        decision = master_agent.make_decision(health_analysis, current_appointments)
        return json.dumps(decision)
