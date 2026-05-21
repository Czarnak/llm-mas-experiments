import asyncio
import random
import time
from datetime import datetime
from typing import List, Dict, Any

# Data models

class SensorData:
    def __init__(self, sensor_id: str, cockroach_count: int, location: str, timestamp: str):
        self.sensor_id = sensor_id
        self.cockroach_count = cockroach_count
        self.location = location
        self.timestamp = timestamp

    def to_dict(self) -> Dict[str, Any]:
        return {
            'sensor_id': self.sensor_id,
            'cockroach_count': self.cockroach_count,
            'location': self.location,
            'timestamp': self.timestamp
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SensorData':
        return cls(data['sensor_id'], data['cockroach_count'], data['location'], data['timestamp'])


class AlertDetails:
    def __init__(self, location: str, cockroach_count: int, timestamp: str):
        self.location = location
        self.cockroach_count = cockroach_count
        self.timestamp = timestamp

    def to_dict(self) -> Dict[str, Any]:
        return {
            'location': self.location,
            'cockroach_count': self.cockroach_count,
            'timestamp': self.timestamp
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AlertDetails':
        return cls(data['location'], data['cockroach_count'], data['timestamp'])


class HighActivityZone:
    def __init__(self, location: str, cockroach_count: int, timestamp: str):
        self.location = location
        self.cockroach_count = cockroach_count
        self.timestamp = timestamp

    def to_dict(self) -> Dict[str, Any]:
        return {
            'location': self.location,
            'cockroach_count': self.cockroach_count,
            'timestamp': self.timestamp
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'HighActivityZone':
        return cls(data['location'], data['cockroach_count'], data['timestamp'])


# Component implementations

class SensorNode:
    def __init__(self, sensor_id: str, location: str):
        self.sensor_id = sensor_id
        self.location = location
        self.data_queue = asyncio.Queue()
        
    async def run(self):
        print(f"SensorNode {self.sensor_id} starting at location {self.location}")
        
        while True:
            # Simulate sensor data
            cockroach_count = random.randint(0, 10)  # Random cockroach count
            
            # Create sensor data
            sensor_data = SensorData(
                sensor_id=self.sensor_id,
                cockroach_count=cockroach_count,
                location=self.location,
                timestamp=datetime.now().isoformat()
            )
            
            # Add to queue for CentralCoordinator
            await self.data_queue.put(sensor_data)
            
            print(f"SensorNode {self.sensor_id} sent data: {cockroach_count} cockroaches at {self.location}")
            
            # Wait for next period (10 seconds)
            await asyncio.sleep(10)


class CentralCoordinator:
    def __init__(self):
        self.aggregated_data: Dict[str, List[SensorData]] = {}
        self.high_activity_zones: List[HighActivityZone] = []
        self.data_queue = asyncio.Queue()
        self.pattern_queue = asyncio.Queue()
        self.alert_queue = asyncio.Queue()
        
    async def run(self):
        print("CentralCoordinator starting")
        
        # Process incoming sensor data
        while True:
            try:
                # Get data from sensor nodes
                sensor_data = await asyncio.wait_for(self.data_queue.get(), timeout=1.0)
                print(f"CentralCoordinator received data from {sensor_data.sensor_id}")
                
                # Aggregate data
                if sensor_data.sensor_id not in self.aggregated_data:
                    self.aggregated_data[sensor_data.sensor_id] = []
                
                self.aggregated_data[sensor_data.sensor_id].append(sensor_data)
                
                # Send to PatternRecognitionModule
                await self.pattern_queue.put(sensor_data)
                
                # Analyze data periodically
                await self.analyze_data()
                
            except asyncio.TimeoutError:
                # No data received, continue
                pass
            
            # Small delay to prevent busy waiting
            await asyncio.sleep(0.1)

    async def analyze_data(self):
        # In a real system, this would be more complex
        # For now, we'll just identify high activity zones based on recent data
        
        # Simple algorithm: if a location has > 5 cockroaches in last 3 readings
        high_activity_locations = {}
        
        for sensor_id, readings in self.aggregated_data.items():
            if len(readings) >= 3:  # At least 3 readings
                recent_count = sum([r.cockroach_count for r in readings[-3:]])
                if recent_count > 5:
                    location = readings[-1].location
                    if location not in high_activity_locations:
                        high_activity_locations[location] = 0
                    high_activity_locations[location] += recent_count
        
        # Update high activity zones
        self.high_activity_zones = [
            HighActivityZone(loc, count, datetime.now().isoformat())
            for loc, count in high_activity_locations.items()
        ]
        
        # Send high activity zones to NotificationService
        if self.high_activity_zones:
            for zone in self.high_activity_zones:
                alert = AlertDetails(zone.location, zone.cockroach_count, zone.timestamp)
                await self.alert_queue.put(alert)
                
            print(f"CentralCoordinator identified high activity zones: {[z.location for z in self.high_activity_zones]}")


class PatternRecognitionModule:
    def __init__(self):
        self.data_queue = asyncio.Queue()
        self.coordinator_queue = asyncio.Queue()
        
    async def run(self):
        print("PatternRecognitionModule starting")
        
        while True:
            try:
                # Get data from CentralCoordinator
                sensor_data = await asyncio.wait_for(self.data_queue.get(), timeout=1.0)
                print("PatternRecognitionModule analyzing activity patterns")
                
                # In a real system, this would perform complex pattern recognition
                # For simulation, we'll just pass the data along
                
                # Send to CentralCoordinator (in a real system this would be more complex)
                await self.coordinator_queue.put(sensor_data)
                
            except asyncio.TimeoutError:
                # No data received, continue
                pass
            
            # Small delay to prevent busy waiting
            await asyncio.sleep(0.1)


class NotificationService:
    def __init__(self):
        self.alert_queue = asyncio.Queue()
        self.admin_queue = asyncio.Queue()
        self.pest_queue = asyncio.Queue()
        self.student_queue = asyncio.Queue()
        
    async def run(self):
        print("NotificationService starting")
        
        while True:
            try:
                # Get alert from CentralCoordinator
                alert = await asyncio.wait_for(self.alert_queue.get(), timeout=1.0)
                print("NotificationService received high activity zone alert")
                
                # Send to Building Administration
                await self.admin_queue.put(alert)
                
                # Send to Pest Control Company
                await self.pest_queue.put(alert)
                
                # Send to Student Residents
                await self.student_queue.put(alert)
                
                print(f"NotificationService sent alerts for {alert.location}")
                
            except asyncio.TimeoutError:
                # No alert received, continue
                pass
            
            # Small delay to prevent busy waiting
            await asyncio.sleep(0.1)


class BuildingAdministration:
    def __init__(self):
        self.alert_queue = asyncio.Queue()
        
    async def run(self):
        print("BuildingAdministration starting")
        
        while True:
            try:
                # Get alert from NotificationService
                alert = await asyncio.wait_for(self.alert_queue.get(), timeout=1.0)
                print("BuildingAdministration received alert")
                
                print(f"Building Administration responding to alert at {alert.location}")
                
                # In a real system, this would trigger administrative actions
                # For simulation, we'll just log the response
                print(f"Building Administration: Alert responded to for {alert.location} with {alert.cockroach_count} cockroaches")
                
            except asyncio.TimeoutError:
                # No alert received, continue
                pass
            
            # Small delay to prevent busy waiting
            await asyncio.sleep(0.1)


class PestControlCompany:
    def __init__(self):
        self.alert_queue = asyncio.Queue()
        
    async def run(self):
        print("PestControlCompany starting")
        
        while True:
            try:
                # Get alert from NotificationService
                alert = await asyncio.wait_for(self.alert_queue.get(), timeout=1.0)
                print("PestControlCompany received alert")
                
                print(f"Pest Control Company responding to alert at {alert.location}")
                
                # In a real system, this would trigger treatment
                # For simulation, we'll just log the treatment
                print(f"Pest Control Company: Treatment executed at {alert.location} with {alert.cockroach_count} cockroaches")
                
            except asyncio.TimeoutError:
                # No alert received, continue
                pass
            
            # Small delay to prevent busy waiting
            await asyncio.sleep(0.1)


class StudentResident:
    def __init__(self, resident_id: str):
        self.resident_id = resident_id
        self.alert_queue = asyncio.Queue()
        
    async def run(self):
        print(f"StudentResident {self.resident_id} starting")
        
        while True:
            try:
                # Get notification from NotificationService
                alert = await asyncio.wait_for(self.alert_queue.get(), timeout=1.0)
                print("Student Resident received notification")
                
                print(f"Student Resident {self.resident_id}: Notification received for {alert.location} with {alert.cockroach_count} cockroaches")
                
                # In a real system, this would trigger user notification
                # For simulation, we'll just log
                print(f"Student Resident {self.resident_id}: Notification processed for {alert.location}")
                
            except asyncio.TimeoutError:
                # No notification received, continue
                pass
            
            # Small delay to prevent busy waiting
            await asyncio.sleep(0.1)


async def run_system():
    print("Starting Multi-Agent System for Cockroach Detection...")
    
    # Create components
    sensor_nodes = []
    for i in range(5):  # 5 sensor nodes
        location = f"Room_{random.randint(1, 100)}"
        sensor_node = SensorNode(f"sensor_{i}", location)
        sensor_nodes.append(sensor_node)
        
    coordinator = CentralCoordinator()
    pattern_module = PatternRecognitionModule()
    notification_service = NotificationService()
    building_admin = BuildingAdministration()
    pest_control = PestControlCompany()
    
    student_residents = []
    for i in range(3):  # 3 student residents
        student = StudentResident(f"resident_{i}")
        student_residents.append(student)
        
    # Create tasks for all components
    tasks = []
    
    # Sensor nodes tasks
    for node in sensor_nodes:
        tasks.append(asyncio.create_task(node.run()))
        
    # Coordinator task
    tasks.append(asyncio.create_task(coordinator.run()))
    
    # Pattern recognition task
    tasks.append(asyncio.create_task(pattern_module.run()))
    
    # Notification service task
    tasks.append(asyncio.create_task(notification_service.run()))
    
    # Building administration task
    tasks.append(asyncio.create_task(building_admin.run()))
    
    # Pest control task
    tasks.append(asyncio.create_task(pest_control.run()))
    
    # Student resident tasks
    for resident in student_residents:
        tasks.append(asyncio.create_task(resident.run()))
        
    # Connect queues
    # Sensor nodes -> Central Coordinator
    for node in sensor_nodes:
        async def forward_sensor_data(node):
            while True:
                data = await node.data_queue.get()
                await coordinator.data_queue.put(data)
        tasks.append(asyncio.create_task(forward_sensor_data(node)))
        
    # Central Coordinator -> Pattern Recognition
    async def forward_pattern_data(coordinator):
        while True:
            data = await coordinator.pattern_queue.get()
            await pattern_module.data_queue.put(data)
    tasks.append(asyncio.create_task(forward_pattern_data(coordinator)))
    
    # Pattern Recognition -> Central Coordinator
    async def forward_pattern_response(pattern_module):
        while True:
            data = await pattern_module.coordinator_queue.get()
            await coordinator.data_queue.put(data)
    tasks.append(asyncio.create_task(forward_pattern_response(pattern_module)))
    
    # Central Coordinator -> Notification Service
    async def forward_alerts(coordinator):
        while True:
            alert = await coordinator.alert_queue.get()
            await notification_service.alert_queue.put(alert)
    tasks.append(asyncio.create_task(forward_alerts(coordinator)))
    
    # Notification Service -> Building Administration
    async def forward_admin_alerts(notification_service):
        while True:
            alert = await notification_service.admin_queue.get()
            await building_admin.alert_queue.put(alert)
    tasks.append(asyncio.create_task(forward_admin_alerts(notification_service)))
    
    # Notification Service -> Pest Control
    async def forward_pest_alerts(notification_service):
        while True:
            alert = await notification_service.pest_queue.get()
            await pest_control.alert_queue.put(alert)
    tasks.append(asyncio.create_task(forward_pest_alerts(notification_service)))
    
    # Notification Service -> Student Residents
    async def forward_student_alerts(notification_service):
        while True:
            alert = await notification_service.student_queue.get()
            for resident in student_residents:
                await resident.alert_queue.put(alert)
    tasks.append(asyncio.create_task(forward_student_alerts(notification_service)))
    
    print("All components started. System running for 60 seconds...")
    
    # Run for 60 seconds
    await asyncio.sleep(60)
    
    # Cancel all tasks
    for task in tasks:
        task.cancel()
    
    print("System stopped.")

if __name__ == "__main__":
    asyncio.run(run_system())