import asyncio
from spade import agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
import json
import random
import time

# Import all agent classes
from vehicle_navigator import VehicleNavigatorAgent
from traffic_light_controller import TrafficLightControllerAgent
from road_condition_reporter import RoadConditionReporterAgent
from driver_alerting_system import DriverAlertingSystemAgent
from navigation_manager import NavigationManagerAgent

async def run_system():
    print("Starting Multi-Agent Traffic Management System...")
    
    # Create agents
    navigation_manager = NavigationManagerAgent("navigation_manager@localhost", "password")
    vehicle_navigator = VehicleNavigatorAgent("vehicle_navigator@localhost", "password")
    traffic_light_controller = TrafficLightControllerAgent("traffic_light@localhost", "password")
    road_condition_reporter = RoadConditionReporterAgent("road_condition@localhost", "password")
    driver_alerting_system = DriverAlertingSystemAgent("driver_alert@localhost", "password")
    
    # Start all agents
    await navigation_manager.start()
    await vehicle_navigator.start()
    await traffic_light_controller.start()
    await road_condition_reporter.start()
    await driver_alerting_system.start()
    
    print("All agents started. System is running...")
    
    # Simulate some activity for 60 seconds
    await asyncio.sleep(60)
    
    # Stop all agents
    await navigation_manager.stop()
    await vehicle_navigator.stop()
    await traffic_light_controller.stop()
    await road_condition_reporter.stop()
    await driver_alerting_system.stop()
    
    print("System stopped.")

if __name__ == "__main__":
    asyncio.run(run_system())