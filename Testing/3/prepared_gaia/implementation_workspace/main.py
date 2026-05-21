# Pet Health Monitoring Multi-Agent System
# Entry point for the system

import os
import json
from dotenv import load_dotenv
from crewai import Agent, Task, Crew

# Load environment variables
load_dotenv()

# Import agents
from agents.sensor_agent import SensorAgent
from agents.smart_collar_agent import SmartCollarAgent
from agents.analyzer_agent import AnalyzerAgent
from agents.master_agent import MasterAgent
from agents.calendar_agent import CalendarAgent

# Import tools
from tools.data_tools import DataGeneratorTool, DataAggregatorTool, DataParserTool, DataAnalyzerTool, AppointmentPlannerTool

# Initialize agents
sensor_agent = SensorAgent()
smart_collar_agent = SmartCollarAgent()
analyzer_agent = AnalyzerAgent()
master_agent = MasterAgent()
calendar_agent = CalendarAgent()

# Create a simple simulation of the multi-agent workflow
if __name__ == "__main__":
    print("Starting Pet Health Monitoring Multi-Agent System...")
    
    # Simulate the workflow as described in GAIA documentation
    try:
        # Step 1: Sensor generates data
        print("\n1. Sensor Simulator generating data...")
        raw_data = sensor_agent.generate_sensor_data()
        print(f"Generated raw data: {json.dumps(raw_data, indent=2)}")
        
        # Step 2: Smart Collar Agent aggregates data
        print("\n2. Smart Collar Agent aggregating data...")
        aggregated_data = smart_collar_agent.aggregate_data([raw_data])
        print(f"Aggregated data: {json.dumps(aggregated_data, indent=2)}")
        
        # Step 3: Smart Collar Agent parses data
        print("\n3. Smart Collar Agent parsing data...")
        parsed_data = smart_collar_agent.parse_data(aggregated_data)
        print(f"Parsed data: {json.dumps(parsed_data, indent=2)}")
        
        # Step 4: Analyzer Agent analyzes data
        print("\n4. Analyzer Agent analyzing data...")
        analysis_result = analyzer_agent.analyze_data(parsed_data)
        print(f"Analysis result: {json.dumps(analysis_result, indent=2)}")
        
        # Step 5: Master Agent makes decision
        print("\n5. Master Agent making decision...")
        current_appointments = calendar_agent.get_current_schedule()
        decision = master_agent.make_decision(analysis_result, current_appointments)
        print(f"Decision: {json.dumps(decision, indent=2)}")
        
        # Step 6: If appointment needed, schedule it
        if decision["action"] == "schedule_appointment":
            print("\n6. Scheduling appointment...")
            appointment = {
                "datetime": "2024-05-25T10:00:00Z",
                "reason": "health_concern",
                "pet": "Buddy",
                "type": "health_checkup"
            }
            scheduled_appointment = calendar_agent.add_appointment(appointment)
            print(f"Scheduled appointment: {json.dumps(scheduled_appointment, indent=2)}")
        
        print("\n=== SYSTEM EXECUTION COMPLETE ===")
        
    except Exception as e:
        print(f"Error during execution: {str(e)}")
        import traceback
        traceback.print_exc()
