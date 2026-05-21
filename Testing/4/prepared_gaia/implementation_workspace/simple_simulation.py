import asyncio
import json
import random
from datetime import datetime

# Simple simulation of the multi-agent system without complex agent communication

class VehicleNavigator:
    def __init__(self):
        self.current_position = "A"
        self.route = None
        
    def get_position(self):
        return self.current_position
        
    def generate_preferred_route(self):
        # Simple route generation logic
        return {
            "start": self.current_position,
            "end": "B",
            "waypoints": [self.current_position, "C", "D", "B"],
            "estimated_time": 15
        }
        
    def update_position(self):
        # Simulate movement
        positions = ["A", "C", "D", "B"]
        if self.current_position in positions:
            current_idx = positions.index(self.current_position)
            next_idx = (current_idx + 1) % len(positions)
            self.current_position = positions[next_idx]


class TrafficLightController:
    def __init__(self):
        self.current_state = "green"
        self.vehicle_position = "A"
        
    def get_state(self):
        return self.current_state
        
    def change_state(self):
        # Toggle between green and red
        if self.current_state == "green":
            self.current_state = "red"
        else:
            self.current_state = "green"
        return self.current_state
        
    def update_vehicle_position(self):
        # Simulate vehicle movement
        positions = ["A", "C", "D", "B"]
        if self.vehicle_position in positions:
            current_idx = positions.index(self.vehicle_position)
            next_idx = (current_idx + 1) % len(positions)
            self.vehicle_position = positions[next_idx]


class RoadConditionReporter:
    def __init__(self):
        self.events = [
            "accident",
            "traffic_jam",
            "road_construction",
            "weather_delay",
            "no_event"
        ]
        
    def get_condition(self):
        return random.choice(self.events)


class DriverAlertingSystem:
    def __init__(self):
        self.alerts = []
        
    def generate_alert(self, route):
        alert = {
            "message": f"Vehicle approaching with route: {route['waypoints']}",
            "time": route["estimated_time"],
            "conditions": "no_event",
            "timestamp": datetime.now().isoformat()
        }
        self.alerts.append(alert)
        return alert


class NavigationManager:
    def __init__(self):
        self.vehicle_positions = {}
        self.traffic_light_states = {}
        self.road_conditions = {}
        self.preferred_routes = {}
        self.route = None
        
    def update_vehicle_position(self, agent_id, position):
        self.vehicle_positions[agent_id] = position
        
    def update_traffic_light_state(self, agent_id, state):
        self.traffic_light_states[agent_id] = state
        
    def update_road_condition(self, agent_id, condition):
        self.road_conditions[agent_id] = condition
        
    def update_preferred_route(self, agent_id, route):
        self.preferred_routes[agent_id] = route
        
    def generate_route(self):
        # Simple route generation logic
        return {
            "start": "A",
            "end": "B",
            "waypoints": ["A", "C", "D", "B"],
            "estimated_time": 15,
            "conditions": self.road_conditions
        }
        
    def get_route(self):
        if self.route:
            return self.route
        else:
            return self.generate_route()

async def run_simulation():
    print("Starting Multi-Agent Traffic Management Simulation...")
    
    # Initialize agents
    navigator = VehicleNavigator()
    traffic_light = TrafficLightController()
    road_reporter = RoadConditionReporter()
    alert_system = DriverAlertingSystem()
    manager = NavigationManager()
    
    print("Agents initialized.")
    
    # Simulate 10 time steps
    for step in range(10):
        print(f"\n--- Time Step {step + 1} ---")
        
        # Vehicle Navigator behavior
        position = navigator.get_position()
        print(f"Vehicle position: {position}")
        
        # Generate preferred route
        preferred_route = navigator.generate_preferred_route()
        print(f"Preferred route: {preferred_route['waypoints']}")
        
        # Update vehicle position
        navigator.update_position()
        
        # Traffic Light Controller behavior
        light_state = traffic_light.get_state()
        print(f"Traffic light state: {light_state}")
        
        # Change light state periodically
        if step % 3 == 0:  # Change every 3 steps
            new_state = traffic_light.change_state()
            print(f"Traffic light changed to: {new_state}")
            
        # Update vehicle position for traffic light
        traffic_light.update_vehicle_position()
        
        # Road Condition Reporter behavior
        condition = road_reporter.get_condition()
        print(f"Road condition: {condition}")
        
        # Driver Alerting System behavior
        alert = alert_system.generate_alert(preferred_route)
        print(f"Generated alert: {alert['message'][:50]}...")
        
        # Navigation Manager behavior
        manager.update_vehicle_position("vehicle_navigator", position)
        manager.update_traffic_light_state("traffic_light", light_state)
        manager.update_road_condition("road_reporter", condition)
        manager.update_preferred_route("vehicle_navigator", preferred_route)
        
        route = manager.get_route()
        print(f"Generated route: {route['waypoints']}")
        
        # Wait a bit
        await asyncio.sleep(0.5)
        
    print("\nSimulation completed.")

if __name__ == "__main__":
    asyncio.run(run_simulation())