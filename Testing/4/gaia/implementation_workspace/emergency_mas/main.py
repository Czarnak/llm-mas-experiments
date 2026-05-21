# Emergency Vehicle Multi-Agent System
# Based on GAIA methodology for urban emergency vehicle route optimization

import time
import threading
import random
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import json

# Data structures for our system
@dataclass
class Position:
    x: float
    y: float
    
@dataclass
class Vehicle:
    vehicle_id: str
    position: Position
    velocity: float  # km/h
    
@dataclass
class Event:
    event_id: str
    event_type: str  # accident, traffic_jam, etc.
    position: Position
    severity: int  # 1-5 scale
    
@dataclass
class TrafficLight:
    light_id: str
    position: Position
    state: str  # green, yellow, red
    
@dataclass
class Route:
    route_id: str
    waypoints: List[Position]
    estimated_time: float  # minutes
    
@dataclass
class Notification:
    vehicle_id: str
    estimated_arrival_time: float  # minutes from now
    route_path: List[Position]

# Agent base class
class Agent:
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.state = {}
        
    def process_message(self, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        raise NotImplementedError("Subclasses must implement process_message")
        
    def send_message(self, recipient: 'Agent', message: Dict[str, Any]):
        # In a real system, this would go through a message broker
        return recipient.process_message(message)

# Emergency Vehicle Agent
class EmergencyVehicleAgent(Agent):
    def __init__(self, vehicle_id: str, destination: Position):
        super().__init__(f"EmergencyVehicle-{vehicle_id}")
        self.vehicle_id = vehicle_id
        self.destination = destination
        self.current_position = Position(0.0, 0.0)
        self.route_plan = None
        self.adjusted_route_plan = None
        self.estimated_arrival_time = 0.0
        self.is_active = True
        
    def process_message(self, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        msg_type = message.get("type")
        
        if msg_type == "INITIATE_ROUTE_PLANNING":
            # Request route planning from RouteOptimizer
            return {
                "type": "ROUTE_PLAN_REQUEST",
                "sender": self.agent_id,
                "destination": self.destination,
                "vehicle_id": self.vehicle_id
            }
        
        elif msg_type == "ROUTE_PLAN_RESPONSE":
            self.route_plan = message.get("route_plan")
            self.estimated_arrival_time = message.get("estimated_time")
            print(f"{self.agent_id}: Route plan received")
            
            # Request position updates
            return {
                "type": "REQUEST_POSITION_UPDATE",
                "sender": self.agent_id,
                "vehicle_id": self.vehicle_id
            }
            
        elif msg_type == "POSITION_UPDATE_RESPONSE":
            # Process current vehicle and other vehicle positions
            self.current_position = message.get("current_position")
            print(f"{self.agent_id}: Position updated to {self.current_position}")
            
            # Request route adjustment if needed
            return {
                "type": "REQUEST_ROUTE_ADJUSTMENT",
                "sender": self.agent_id,
                "current_position": self.current_position,
                "traffic_conditions": message.get("traffic_conditions")
            }
            
        elif msg_type == "ROUTE_ADJUSTMENT_RESPONSE":
            self.adjusted_route_plan = message.get("adjusted_route_plan")
            print(f"{self.agent_id}: Route adjusted")
            
            # Request light adjustment if approaching traffic light
            return {
                "type": "REQUEST_LIGHT_ADJUSTMENT",
                "sender": self.agent_id,
                "traffic_light_id": message.get("traffic_light_id"),
                "estimated_arrival_time": self.estimated_arrival_time
            }
            
        elif msg_type == "LIGHT_ADJUSTMENT_RESPONSE":
            print(f"{self.agent_id}: Light timing adjusted")
            return None
        
        return None

# Traffic Monitoring Agent
class TrafficMonitoringAgent(Agent):
    def __init__(self):
        super().__init__("TrafficMonitor")
        self.vehicles = {}
        self.events = {}
        self.traffic_lights = {}
        
    def process_message(self, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        msg_type = message.get("type")
        
        if msg_type == "REQUEST_POSITION_UPDATE":
            vehicle_id = message.get("vehicle_id")
            # Simulate getting position data
            if vehicle_id in self.vehicles:
                return {
                    "type": "POSITION_UPDATE_RESPONSE",
                    "sender": self.agent_id,
                    "vehicle_id": vehicle_id,
                    "current_position": self.vehicles[vehicle_id].position,
                    "other_vehicles": list(self.vehicles.values()),
                    "traffic_conditions": self._get_traffic_conditions()
                }
            
        elif msg_type == "REPORT_EVENT":
            # Simulate reporting events
            event = Event(
                event_id=message.get("event_id"),
                event_type=message.get("event_type"),
                position=message.get("position"),
                severity=message.get("severity")
            )
            self.events[event.event_id] = event
            print(f"{self.agent_id}: Event reported: {event.event_type}")
            
            # Report to RouteOptimizer
            return {
                "type": "EVENT_REPORTED",
                "sender": self.agent_id,
                "event": event
            }
        
        return None
    
    def _get_traffic_conditions(self) -> Dict[str, Any]:
        # Simulate traffic conditions
        return {
            "congestion_level": random.randint(1, 5),
            "average_speed": random.randint(20, 60)
        }

# Route Optimization Agent
class RouteOptimizationAgent(Agent):
    def __init__(self):
        super().__init__("RouteOptimizer")
        self.routes = {}
        
    def process_message(self, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        msg_type = message.get("type")
        
        if msg_type == "ROUTE_PLAN_REQUEST":
            destination = message.get("destination")
            vehicle_id = message.get("vehicle_id")
            
            # Generate a simple route
            route = Route(
                route_id=f"route-{vehicle_id}",
                waypoints=[Position(0.0, 0.0), Position(5.0, 3.0), destination],
                estimated_time=15.0  # minutes
            )
            self.routes[route.route_id] = route
            
            return {
                "type": "ROUTE_PLAN_RESPONSE",
                "sender": self.agent_id,
                "vehicle_id": vehicle_id,
                "route_plan": route,
                "estimated_time": route.estimated_time
            }
            
        elif msg_type == "REQUEST_ROUTE_ADJUSTMENT":
            current_position = message.get("current_position")
            traffic_conditions = message.get("traffic_conditions")
            
            # Simulate route adjustment
            adjusted_route = Route(
                route_id=f"adjusted-route-{random.randint(1000, 9999)}",
                waypoints=[Position(0.0, 0.0), Position(4.0, 2.0), Position(8.0, 4.0), destination],
                estimated_time=12.0  # minutes
            )
            
            return {
                "type": "ROUTE_ADJUSTMENT_RESPONSE",
                "sender": self.agent_id,
                "adjusted_route_plan": adjusted_route,
                "traffic_light_id": f"light-{random.randint(1, 10)}"
            }
        
        return None

# Traffic Light Control Agent
class TrafficLightControlAgent(Agent):
    def __init__(self):
        super().__init__("TrafficLightController")
        self.lights = {}
        
    def process_message(self, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        msg_type = message.get("type")
        
        if msg_type == "REQUEST_LIGHT_ADJUSTMENT":
            light_id = message.get("traffic_light_id")
            estimated_arrival_time = message.get("estimated_arrival_time")
            
            # Adjust light timing
            adjusted_timing = {
                "light_id": light_id,
                "new_timing": estimated_arrival_time + 2.0  # Add 2 minutes
            }
            
            return {
                "type": "LIGHT_ADJUSTMENT_RESPONSE",
                "sender": self.agent_id,
                "adjusted_light_timing": adjusted_timing
            }
        
        return None

# Driver Notification Agent
class DriverNotificationAgent(Agent):
    def __init__(self):
        super().__init__("DriverNotifier")
        self.notifications = []
        
    def process_message(self, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        msg_type = message.get("type")
        
        if msg_type == "SEND_NOTIFICATION":
            notification = Notification(
                vehicle_id=message.get("vehicle_id"),
                estimated_arrival_time=message.get("estimated_arrival_time"),
                route_path=message.get("route_path")
            )
            self.notifications.append(notification)
            
            print(f"{self.agent_id}: Notification sent for vehicle {notification.vehicle_id}")
            
            return {
                "type": "NOTIFICATION_SENT",
                "sender": self.agent_id,
                "notification_id": f"notif-{len(self.notifications)}"
            }
        
        return None

# Message Broker
class MessageBroker:
    def __init__(self):
        self.agents = {}
        self.message_queue = []
        
    def register_agent(self, agent: Agent):
        self.agents[agent.agent_id] = agent
        
    def send_message(self, sender_id: str, recipient_id: str, message: Dict[str, Any]):
        if recipient_id in self.agents:
            agent = self.agents[recipient_id]
            response = agent.process_message(message)
            
            # If there's a response, send it back
            if response:
                self.send_message(recipient_id, sender_id, response)
            
            return response
        return None

# Simulation Manager
class SimulationManager:
    def __init__(self):
        self.message_broker = MessageBroker()
        self.agents = {}
        self.running = False
        
    def setup_agents(self):
        # Create agents
        emergency_vehicle = EmergencyVehicleAgent("EV-001", Position(10.0, 10.0))
        traffic_monitor = TrafficMonitoringAgent()
        route_optimizer = RouteOptimizationAgent()
        traffic_light_controller = TrafficLightControlAgent()
        driver_notifier = DriverNotificationAgent()
        
        # Register agents
        self.message_broker.register_agent(emergency_vehicle)
        self.message_broker.register_agent(traffic_monitor)
        self.message_broker.register_agent(route_optimizer)
        self.message_broker.register_agent(traffic_light_controller)
        self.message_broker.register_agent(driver_notifier)
        
        self.agents = {
            "emergency_vehicle": emergency_vehicle,
            "traffic_monitor": traffic_monitor,
            "route_optimizer": route_optimizer,
            "traffic_light_controller": traffic_light_controller,
            "driver_notifier": driver_notifier
        }
        
    def start_simulation(self):
        print("Starting Emergency Vehicle Multi-Agent System Simulation")
        print("====================================================")
        
        # Start with route planning
        emergency_vehicle = self.agents["emergency_vehicle"]
        
        # Send initial route planning request
        message = {
            "type": "INITIATE_ROUTE_PLANNING",
            "sender": "system"
        }
        
        self.message_broker.send_message("system", emergency_vehicle.agent_id, message)
        
        # Simulate some events
        traffic_monitor = self.agents["traffic_monitor"]
        
        # Report a traffic jam
        traffic_jam_message = {
            "type": "REPORT_EVENT",
            "sender": "system",
            "event_id": "event-001",
            "event_type": "traffic_jam",
            "position": Position(3.0, 2.0),
            "severity": 4
        }
        
        self.message_broker.send_message("system", traffic_monitor.agent_id, traffic_jam_message)
        
        print("Simulation completed")
        
    def run(self):
        self.setup_agents()
        self.start_simulation()

# Main execution
if __name__ == "__main__":
    simulation = SimulationManager()
    simulation.run()