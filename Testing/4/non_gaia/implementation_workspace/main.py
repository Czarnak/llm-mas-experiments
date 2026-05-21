import threading
import time
import random
import json
from dataclasses import dataclass
from typing import List, Dict, Any
from queue import Queue

class Message:
    def __init__(self, sender: str, recipient: str, content: Dict[str, Any], msg_type: str):
        self.sender = sender
        self.recipient = recipient
        self.content = content
        self.msg_type = msg_type

    def __repr__(self):
        return f"Message({self.sender} -> {self.recipient}, {self.msg_type})"

class MessageBroker:
    def __init__(self):
        self.queues: Dict[str, Queue] = {}
        self.lock = threading.Lock()

    def register_agent(self, agent_id: str):
        with self.lock:
            if agent_id not in self.queues:
                self.queues[agent_id] = Queue()

    def send_message(self, message: Message):
        with self.lock:
            if message.recipient in self.queues:
                self.queues[message.recipient].put(message)

    def receive_message(self, agent_id: str, timeout: float = 1.0):
        try:
            return self.queues[agent_id].get(timeout=timeout)
        except:
            return None

class Agent:
    def __init__(self, agent_id: str, broker: MessageBroker):
        self.agent_id = agent_id
        self.broker = broker
        self.broker.register_agent(agent_id)
        self.running = False
        self.thread = None

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()

    def run(self):
        while self.running:
            message = self.broker.receive_message(self.agent_id, timeout=0.1)
            if message:
                self.handle_message(message)
            time.sleep(0.01)

    def handle_message(self, message: Message):
        # Override in subclasses
        pass

@dataclass
class Position:
    x: float
    y: float

@dataclass
class Vehicle:
    vehicle_id: str
    position: Position
    speed: float
    destination: Position
    is_special: bool = False

@dataclass
class TrafficEvent:
    event_id: str
    position: Position
    event_type: str  # "accident", "traffic_jam", "road_work"
    severity: int  # 1-5
    duration: int  # minutes

@dataclass
class TrafficLight:
    light_id: str
    position: Position
    state: str  # "red", "yellow", "green"
    duration: int  # seconds

# Agent classes

class VehicleAgent(Agent):
    def __init__(self, agent_id: str, broker: MessageBroker, vehicle: Vehicle):
        super().__init__(agent_id, broker)
        self.vehicle = vehicle
        self.route = []
        self.current_route_index = 0
        self.broker.register_agent(f"route_{agent_id}")
        self.broker.register_agent(f"event_{agent_id}")

    def handle_message(self, message: Message):
        if message.msg_type == "position_update":
            self.vehicle.position = Position(**message.content["position"])
        elif message.msg_type == "route_update":
            self.route = message.content["route"]
            self.current_route_index = 0
        elif message.msg_type == "traffic_light":
            # Handle traffic light update
            pass
        elif message.msg_type == "event_update":
            # Handle event update
            pass

    def update_position(self):
        # Simple movement simulation
        if self.route and self.current_route_index < len(self.route):
            target = self.route[self.current_route_index]
            # Move towards target
            if abs(self.vehicle.position.x - target.x) > 0.1:
                self.vehicle.position.x += (target.x - self.vehicle.position.x) * 0.05
            if abs(self.vehicle.position.y - target.y) > 0.1:
                self.vehicle.position.y += (target.y - self.vehicle.position.y) * 0.05
            
            # Check if reached target
            if abs(self.vehicle.position.x - target.x) < 0.1 and abs(self.vehicle.position.y - target.y) < 0.1:
                self.current_route_index += 1

    def run(self):
        while self.running:
            self.update_position()
            # Send position update to traffic management
            self.broker.send_message(Message(
                sender=self.agent_id,
                recipient="traffic_management",
                content={"position": {"x": self.vehicle.position.x, "y": self.vehicle.position.y}, "vehicle_id": self.vehicle.vehicle_id},
                msg_type="position_update"
            ))
            time.sleep(0.5)

class TrafficManagementAgent(Agent):
    def __init__(self, agent_id: str, broker: MessageBroker):
        super().__init__(agent_id, broker)
        self.vehicles: Dict[str, Vehicle] = {}
        self.traffic_lights: Dict[str, TrafficLight] = {}
        self.events: List[TrafficEvent] = []
        self.map_size = (100, 100)

    def handle_message(self, message: Message):
        if message.msg_type == "position_update":
            vehicle_id = message.content["vehicle_id"]
            self.vehicles[vehicle_id] = Vehicle(
                vehicle_id=vehicle_id,
                position=Position(**message.content["position"]),
                speed=30.0,
                destination=Position(90, 90),
                is_special=vehicle_id.startswith("special")
            )
        elif message.msg_type == "traffic_light_update":
            light_id = message.content["light_id"]
            self.traffic_lights[light_id] = TrafficLight(
                light_id=light_id,
                position=Position(**message.content["position"]),
                state=message.content["state"],
                duration=message.content["duration"]
            )
        elif message.msg_type == "event_update":
            event = TrafficEvent(
                event_id=message.content["event_id"],
                position=Position(**message.content["position"]),
                event_type=message.content["event_type"],
                severity=message.content["severity"],
                duration=message.content["duration"]
            )
            self.events.append(event)
            # Notify all vehicles about the event
            for vehicle_id in self.vehicles:
                self.broker.send_message(Message(
                    sender=self.agent_id,
                    recipient=f"vehicle_{vehicle_id}",
                    content=message.content,
                    msg_type="event_update"
                ))

    def generate_route(self, vehicle_id: str, destination: Position) -> List[Position]:
        # Simple straight-line route generation
        start = self.vehicles[vehicle_id].position
        route = []
        steps = 10
        for i in range(steps):
            x = start.x + (destination.x - start.x) * i / steps
            y = start.y + (destination.y - start.y) * i / steps
            route.append(Position(x, y))
        return route

    def update_traffic_lights(self):
        # Simple traffic light simulation
        for light_id, light in self.traffic_lights.items():
            # Change state every 10 seconds
            if time.time() % 30 < 10:
                new_state = "green"
            elif time.time() % 30 < 20:
                new_state = "yellow"
            else:
                new_state = "red"
            
            if light.state != new_state:
                light.state = new_state
                # Notify vehicles
                for vehicle_id in self.vehicles:
                    self.broker.send_message(Message(
                        sender=self.agent_id,
                        recipient=f"vehicle_{vehicle_id}",
                        content={"light_id": light_id, "state": new_state},
                        msg_type="traffic_light"
                    ))

    def check_events(self):
        # Remove expired events
        current_time = time.time()
        self.events = [event for event in self.events if current_time - event.duration * 60 < 0]

    def run(self):
        while self.running:
            self.update_traffic_lights()
            self.check_events()
            time.sleep(1)

class EventMonitoringAgent(Agent):
    def __init__(self, agent_id: str, broker: MessageBroker):
        super().__init__(agent_id, broker)
        self.events: List[TrafficEvent] = []

    def handle_message(self, message: Message):
        pass

    def generate_random_event(self):
        # Generate random traffic event
        event_types = ["accident", "traffic_jam", "road_work"]
        event_type = random.choice(event_types)
        severity = random.randint(1, 5)
        duration = random.randint(10, 60)  # minutes
        
        # Generate random position
        position = Position(
            random.uniform(0, 100),
            random.uniform(0, 100)
        )
        
        event = TrafficEvent(
            event_id=f"event_{len(self.events) + 1}",
            position=position,
            event_type=event_type,
            severity=severity,
            duration=duration
        )
        self.events.append(event)
        
        # Notify traffic management
        self.broker.send_message(Message(
            sender=self.agent_id,
            recipient="traffic_management",
            content={
                "event_id": event.event_id,
                "position": {"x": event.position.x, "y": event.position.y},
                "event_type": event.event_type,
                "severity": event.severity,
                "duration": event.duration
            },
            msg_type="event_update"
        ))

    def run(self):
        while self.running:
            # Generate events randomly
            if random.random() < 0.1:  # 10% chance each second
                self.generate_random_event()
            time.sleep(5)

class NotificationAgent(Agent):
    def __init__(self, agent_id: str, broker: MessageBroker):
        super().__init__(agent_id, broker)
        self.notifications = []

    def handle_message(self, message: Message):
        if message.msg_type == "notification":
            self.notifications.append(message.content)
            print(f"Notification sent to vehicle {message.content['vehicle_id']}: {message.content['message']}")

    def run(self):
        while self.running:
            time.sleep(1)

# Main system

def main():
    print("Starting Multi-Agent Traffic Management System...")
    
    # Initialize message broker
    broker = MessageBroker()
    
    # Create agents
    traffic_management = TrafficManagementAgent("traffic_management", broker)
    event_monitor = EventMonitoringAgent("event_monitor", broker)
    notification_agent = NotificationAgent("notification", broker)
    
    # Create vehicles
    vehicles = [
        Vehicle("vehicle_1", Position(10, 10), 30.0, Position(90, 90)),
        Vehicle("vehicle_2", Position(20, 20), 30.0, Position(90, 90)),
        Vehicle("special_1", Position(5, 5), 40.0, Position(90, 90), is_special=True),
    ]
    
    # Create vehicle agents
    vehicle_agents = []
    for vehicle in vehicles:
        agent = VehicleAgent(f"vehicle_{vehicle.vehicle_id}", broker, vehicle)
        vehicle_agents.append(agent)
        
    # Start all agents
    traffic_management.start()
    event_monitor.start()
    notification_agent.start()
    
    for agent in vehicle_agents:
        agent.start()
    
    # Simulate system running for 30 seconds
    print("System running for 30 seconds...")
    time.sleep(30)
    
    # Stop all agents
    traffic_management.stop()
    event_monitor.stop()
    notification_agent.stop()
    
    for agent in vehicle_agents:
        agent.stop()
    
    print("System stopped.")

if __name__ == "__main__":
    main()