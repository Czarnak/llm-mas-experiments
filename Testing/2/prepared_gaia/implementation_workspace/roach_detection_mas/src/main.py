import asyncio
import json
import random
import time
from datetime import datetime
from typing import Dict, List, Any

# Message types
SENSOR_DATA_MSG = "sensor_data"
ROACH_DETECTION_MSG = "roach_detection"
ROACH_PREDICTION_MSG = "roach_prediction"
NOTIFICATION_MSG = "notification"
DISINFECTION_MSG = "disinfection"
ACKNOWLEDGE_MSG = "acknowledge"

# Agent classes

class SensorDataMessage:
    def __init__(self, room_id, temperature, humidity, waste, movement):
        self.room_id = room_id
        self.temperature = temperature
        self.humidity = humidity
        self.waste = waste
        self.movement = movement
        self.timestamp = datetime.now().isoformat()

    def to_dict(self):
        return {
            "room_id": self.room_id,
            "temperature": self.temperature,
            "humidity": self.humidity,
            "waste": self.waste,
            "movement": self.movement,
            "timestamp": self.timestamp
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["room_id"],
            data["temperature"],
            data["humidity"],
            data["waste"],
            data["movement"]
        )

class RoachDetectionMessage:
    def __init__(self, room_id, count, location, timestamp):
        self.room_id = room_id
        self.count = count
        self.location = location
        self.timestamp = timestamp

    def to_dict(self):
        return {
            "room_id": self.room_id,
            "count": self.count,
            "location": self.location,
            "timestamp": self.timestamp
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["room_id"],
            data["count"],
            data["location"],
            data["timestamp"]
        )

class RoachPredictionMessage:
    def __init__(self, room_id, probability, conditions):
        self.room_id = room_id
        self.probability = probability
        self.conditions = conditions
        self.timestamp = datetime.now().isoformat()

    def to_dict(self):
        return {
            "room_id": self.room_id,
            "probability": self.probability,
            "conditions": self.conditions,
            "timestamp": self.timestamp
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["room_id"],
            data["probability"],
            data["conditions"]
        )

class NotificationMessage:
    def __init__(self, message_type, content, timestamp):
        self.message_type = message_type
        self.content = content
        self.timestamp = timestamp

    def to_dict(self):
        return {
            "message_type": self.message_type,
            "content": self.content,
            "timestamp": self.timestamp
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["message_type"],
            data["content"],
            data["timestamp"]
        )

class DisinfectionMessage:
    def __init__(self, room_id, timestamp):
        self.room_id = room_id
        self.timestamp = timestamp

    def to_dict(self):
        return {
            "room_id": self.room_id,
            "timestamp": self.timestamp
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["room_id"],
            data["timestamp"]
        )

class AcknowledgeMessage:
    def __init__(self, message_id, timestamp):
        self.message_id = message_id
        self.timestamp = timestamp

    def to_dict(self):
        return {
            "message_id": self.message_id,
            "timestamp": self.timestamp
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["message_id"],
            data["timestamp"]
        )

# Message Broker for simulating communication between agents

class MessageBroker:
    def __init__(self):
        self.queues = {}
        
    def register_agent(self, agent_name: str):
        self.queues[agent_name] = asyncio.Queue()
        
    def send_message(self, from_agent: str, to_agent: str, message: Dict[str, Any]):
        if to_agent in self.queues:
            # Add the sender info to the message
            message['from'] = from_agent
            self.queues[to_agent].put_nowait(message)
            print(f"Message sent from {from_agent} to {to_agent}: {message['subject']}")
        else:
            print(f"Warning: No queue for agent {to_agent}")
            
    async def receive_message(self, agent_name: str) -> Dict[str, Any]:
        if agent_name in self.queues:
            return await self.queues[agent_name].get()
        else:
            raise Exception(f"No queue for agent {agent_name}")

# Agent classes based on GAIA roles

class DetectionAgent:
    """
    Wykrywanie karaluchów (WK) - Monitoruje pokoje pod kątem ruchu i inicjuje procedury interwencyjne
    """
    def __init__(self, name: str, broker: MessageBroker):
        self.name = name
        self.broker = broker
        self.broker.register_agent(name)
        self.room_id = "room_101"
        
    async def update_dorm_readings(self):
        # Simulate receiving sensor data
        await asyncio.sleep(1)
        
        # In a real implementation, this would receive actual sensor data
        # For now, we'll simulate it
        sensor_data = SensorDataMessage(
            room_id=self.room_id,
            temperature=random.uniform(20, 25),
            humidity=random.uniform(40, 60),
            waste=random.uniform(0, 10),
            movement=random.uniform(0, 100)
        )
        
        # Send sensor data to SIM agent
        self.broker.send_message(self.name, "sim", {
            "subject": SENSOR_DATA_MSG,
            "body": json.dumps(sensor_data.to_dict())
        })
        
        # Send acknowledge
        self.broker.send_message(self.name, "sim", {
            "subject": ACKNOWLEDGE_MSG,
            "body": json.dumps(AcknowledgeMessage("sensor_data_1", datetime.now().isoformat()).to_dict())
        })

    async def detector(self):
        # This behaviour listens for sensor data and detects roaches
        await asyncio.sleep(1)
        
        # Simulate detection logic
        if random.random() > 0.8:  # 20% chance of detection
            detection = RoachDetectionMessage(
                room_id=self.room_id,
                count=random.randint(1, 5),
                location="corner",
                timestamp=datetime.now().isoformat()
            )
            
            # Send detection message to IS agent
            self.broker.send_message(self.name, "is", {
                "subject": ROACH_DETECTION_MSG,
                "body": json.dumps(detection.to_dict())
            })
            
            # Send disinfection request to WE agent
            self.broker.send_message(self.name, "we", {
                "subject": DISINFECTION_MSG,
                "body": json.dumps(DisinfectionMessage(self.room_id, datetime.now().isoformat()).to_dict())
            })
            
            # Send acknowledge
            self.broker.send_message(self.name, "sim", {
                "subject": ACKNOWLEDGE_MSG,
                "body": json.dumps(AcknowledgeMessage("detection_1", datetime.now().isoformat()).to_dict())
            })

    async def run(self):
        print(f"DetectionAgent {self.name} started")
        
        while True:
            await self.update_dorm_readings()
            await self.detector()
            await asyncio.sleep(2)  # Wait 2 seconds between iterations


class PredictionAgent:
    """
    Przewidywanie karaluchów (PK) - Analizuje parametry środowiskowe w celu estymacji ryzyka wystąpienia szkodników
    """
    def __init__(self, name: str, broker: MessageBroker):
        self.name = name
        self.broker = broker
        self.broker.register_agent(name)
        self.room_id = "room_101"
        
    async def update_dorm_readings(self):
        # Simulate receiving sensor data
        await asyncio.sleep(1)
        
        # In a real implementation, this would receive actual sensor data
        sensor_data = SensorDataMessage(
            room_id=self.room_id,
            temperature=random.uniform(20, 25),
            humidity=random.uniform(40, 60),
            waste=random.uniform(0, 10),
            movement=random.uniform(0, 100)
        )
        
        # Send sensor data to SIM agent
        self.broker.send_message(self.name, "sim", {
            "subject": SENSOR_DATA_MSG,
            "body": json.dumps(sensor_data.to_dict())
        })
        
        # Send acknowledge
        self.broker.send_message(self.name, "sim", {
            "subject": ACKNOWLEDGE_MSG,
            "body": json.dumps(AcknowledgeMessage("sensor_data_1", datetime.now().isoformat()).to_dict())
        })

    async def predictor(self):
        # This behaviour listens for sensor data and predicts roach probability
        await asyncio.sleep(1)
        
        # Simulate prediction logic
        probability = random.uniform(0.1, 0.9)
        conditions = {
            "temperature": random.uniform(20, 25),
            "humidity": random.uniform(40, 60),
            "waste": random.uniform(0, 10)
        }
        
        prediction = RoachPredictionMessage(
            room_id=self.room_id,
            probability=probability,
            conditions=conditions
        )
        
        # Send prediction to IS agent
        self.broker.send_message(self.name, "is", {
            "subject": ROACH_PREDICTION_MSG,
            "body": json.dumps(prediction.to_dict())
        })
        
        # Send acknowledge
        self.broker.send_message(self.name, "sim", {
            "subject": ACKNOWLEDGE_MSG,
            "body": json.dumps(AcknowledgeMessage("prediction_1", datetime.now().isoformat()).to_dict())
        })

    async def run(self):
        print(f"PredictionAgent {self.name} started")
        
        while True:
            await self.update_dorm_readings()
            await self.predictor()
            await asyncio.sleep(2)  # Wait 2 seconds between iterations


class NotificationAgent:
    """
    Informowanie o stanie (IS) - Wysyłanie informacji do administrację i studentów o złym stanie
    """
    def __init__(self, name: str, broker: MessageBroker):
        self.name = name
        self.broker = broker
        self.broker.register_agent(name)
        
    async def my_behav(self):
        # Listen for messages from WK and PK agents
        await asyncio.sleep(1)
        
        # Simulate sending notifications
        notification = NotificationMessage(
            message_type="warning",
            content="Roach detection in room 101",
            timestamp=datetime.now().isoformat()
        )
        
        # Send notification to GUI agent
        self.broker.send_message(self.name, "gui", {
            "subject": NOTIFICATION_MSG,
            "body": json.dumps(notification.to_dict())
        })
        
        # Send acknowledge
        self.broker.send_message(self.name, "sim", {
            "subject": ACKNOWLEDGE_MSG,
            "body": json.dumps(AcknowledgeMessage("notification_1", datetime.now().isoformat()).to_dict())
        })

    async def run(self):
        print(f"NotificationAgent {self.name} started")
        
        while True:
            await self.my_behav()
            await asyncio.sleep(3)  # Wait 3 seconds between iterations


class DisinfectionAgent:
    """
    Wezwanie ekipy dezynsekcyjnej (WE) - Obsługuje zlecenia dezynsekcji i zarządza resetowaniem stanu
    """
    def __init__(self, name: str, broker: MessageBroker):
        self.name = name
        self.broker = broker
        self.broker.register_agent(name)
        
    async def my_behav(self):
        # Listen for disinfection messages
        await asyncio.sleep(1)
        
        # Simulate disinfection process
        notification = NotificationMessage(
            message_type="disinfection",
            content="Disinfection team dispatched to room 101",
            timestamp=datetime.now().isoformat()
        )
        
        # Send notification to GUI agent
        self.broker.send_message(self.name, "gui", {
            "subject": NOTIFICATION_MSG,
            "body": json.dumps(notification.to_dict())
        })
        
        # Send acknowledge
        self.broker.send_message(self.name, "sim", {
            "subject": ACKNOWLEDGE_MSG,
            "body": json.dumps(AcknowledgeMessage("disinfection_1", datetime.now().isoformat()).to_dict())
        })

    async def run(self):
        print(f"DisinfectionAgent {self.name} started")
        
        while True:
            await self.my_behav()
            await asyncio.sleep(4)  # Wait 4 seconds between iterations


class SimulationAgent:
    """
    Symulacja środowiska (SIM) - Generuje dane sensoryczne i aktualizuje stan pokojów
    """
    def __init__(self, name: str, broker: MessageBroker):
        self.name = name
        self.broker = broker
        self.broker.register_agent(name)
        self.room_id = "room_101"
        
    async def my_behav(self):
        # Simulate generating sensor data
        await asyncio.sleep(1)
        
        sensor_data = SensorDataMessage(
            room_id=self.room_id,
            temperature=random.uniform(20, 25),
            humidity=random.uniform(40, 60),
            waste=random.uniform(0, 10),
            movement=random.uniform(0, 100)
        )
        
        # Send sensor data to WK agent
        self.broker.send_message(self.name, "wk", {
            "subject": SENSOR_DATA_MSG,
            "body": json.dumps(sensor_data.to_dict())
        })
        
        # Send sensor data to PK agent
        self.broker.send_message(self.name, "pk", {
            "subject": SENSOR_DATA_MSG,
            "body": json.dumps(sensor_data.to_dict())
        })
        
        # Send notification to GUI agent
        notification = NotificationMessage(
            message_type="sensor_data",
            content="Sensor data updated for room 101",
            timestamp=datetime.now().isoformat()
        )
        
        self.broker.send_message(self.name, "gui", {
            "subject": NOTIFICATION_MSG,
            "body": json.dumps(notification.to_dict())
        })

    async def reset_room_behaviour(self):
        # Simulate room reset
        await asyncio.sleep(10)
        
        # Reset room conditions
        print("Room conditions reset")

    async def run(self):
        print(f"SimulationAgent {self.name} started")
        
        while True:
            await self.my_behav()
            await asyncio.sleep(2)  # Wait 2 seconds between iterations


class GUIAgent:
    """
    Prezentacja danych (GUI) - Odpowiada za zbieranie powiadomień i ich wizualizację
    """
    def __init__(self, name: str, broker: MessageBroker):
        self.name = name
        self.broker = broker
        self.broker.register_agent(name)
        
    async def event_collector(self):
        # Listen for notifications from all agents
        await asyncio.sleep(1)
        
        # Simulate collecting events
        print("GUI: Collecting events from agents")

    async def run(self):
        print(f"GUIAgent {self.name} started")
        
        while True:
            await self.event_collector()
            await asyncio.sleep(1)  # Wait 1 second between iterations

async def run_system():
    print("Starting Multi-Agent System for Roach Detection...")
    
    # Create message broker
    broker = MessageBroker()
    
    # Create agents
    wk_agent = DetectionAgent("wk", broker)
    pk_agent = PredictionAgent("pk", broker)
    is_agent = NotificationAgent("is", broker)
    we_agent = DisinfectionAgent("we", broker)
    sim_agent = SimulationAgent("sim", broker)
    gui_agent = GUIAgent("gui", broker)
    
    # Start agents as tasks
    tasks = [
        asyncio.create_task(wk_agent.run()),
        asyncio.create_task(pk_agent.run()),
        asyncio.create_task(is_agent.run()),
        asyncio.create_task(we_agent.run()),
        asyncio.create_task(sim_agent.run()),
        asyncio.create_task(gui_agent.run())
    ]
    
    print("All agents started. Press Ctrl+C to stop.")
    
    # Keep system running
    try:
        await asyncio.gather(*tasks)
    except KeyboardInterrupt:
        print("Stopping agents...")
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        print("All agents stopped.")

if __name__ == "__main__":
    asyncio.run(run_system())