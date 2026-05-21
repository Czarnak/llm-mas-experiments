import asyncio
import random
import time
from datetime import datetime
from spade import agent
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour
from spade.message import Message
from spade.template import Template

# Data models

class SensorData:
    def __init__(self, sensor_id, cockroach_count, location, timestamp):
        self.sensor_id = sensor_id
        self.cockroach_count = cockroach_count
        self.location = location
        self.timestamp = timestamp

    def to_dict(self):
        return {
            'sensor_id': self.sensor_id,
            'cockroach_count': self.cockroach_count,
            'location': self.location,
            'timestamp': self.timestamp
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['sensor_id'], data['cockroach_count'], data['location'], data['timestamp'])


class AlertDetails:
    def __init__(self, location, cockroach_count, timestamp):
        self.location = location
        self.cockroach_count = cockroach_count
        self.timestamp = timestamp

    def to_dict(self):
        return {
            'location': self.location,
            'cockroach_count': self.cockroach_count,
            'timestamp': self.timestamp
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['location'], data['cockroach_count'], data['timestamp'])


class HighActivityZone:
    def __init__(self, location, cockroach_count, timestamp):
        self.location = location
        self.cockroach_count = cockroach_count
        self.timestamp = timestamp

    def to_dict(self):
        return {
            'location': self.location,
            'cockroach_count': self.cockroach_count,
            'timestamp': self.timestamp
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['location'], data['cockroach_count'], data['timestamp'])


# Agent implementations

class SensorNodeAgent(agent.Agent):
    def __init__(self, jid, password, sensor_id, location):
        super().__init__(jid, password)
        self.sensor_id = sensor_id
        self.location = location

    async def setup(self):
        print(f"SensorNodeAgent {self.sensor_id} starting at location {self.location}")
        
        # Add behaviour to periodically send sensor data
        send_data_behaviour = self.SendSensorDataBehaviour()
        self.add_behaviour(send_data_behaviour)

    class SendSensorDataBehaviour(CyclicBehaviour):
        async def run(self):
            # Simulate sensor data
            cockroach_count = random.randint(0, 10)  # Random cockroach count
            
            # Create sensor data
            sensor_data = SensorData(
                sensor_id=self.agent.sensor_id,
                cockroach_count=cockroach_count,
                location=self.agent.location,
                timestamp=datetime.now().isoformat()
            )
            
            # Send to CentralCoordinator
            msg = Message(to="central_coordinator@localhost", 
                          subject="SensorData",
                          body=str(sensor_data.to_dict()))
            await self.send(msg)
            
            print(f"SensorNode {self.agent.sensor_id} sent data: {cockroach_count} cockroaches at {self.agent.location}")
            
            # Wait for next period (10 seconds)
            await asyncio.sleep(10)


class CentralCoordinatorAgent(agent.Agent):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.aggregated_data = {}
        self.high_activity_zones = []

    async def setup(self):
        print("CentralCoordinatorAgent starting")
        
        # Add behaviour to receive sensor data
        receive_data_behaviour = self.ReceiveSensorDataBehaviour()
        self.add_behaviour(receive_data_behaviour)
        
        # Add behaviour to periodically analyze data
        analyze_behaviour = self.AnalyzeDataBehaviour()
        self.add_behaviour(analyze_behaviour)

    class ReceiveSensorDataBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg and msg.get_metadata("subject") == "SensorData":
                print(f"CentralCoordinator received data from {msg.sender}")
                
                # Parse sensor data
                sensor_data = SensorData.from_dict(eval(msg.body))
                
                # Aggregate data
                if sensor_data.sensor_id not in self.agent.aggregated_data:
                    self.agent.aggregated_data[sensor_data.sensor_id] = []
                
                self.agent.aggregated_data[sensor_data.sensor_id].append(sensor_data)
                
                # Send to PatternRecognitionModule
                msg_to_pattern = Message(to="pattern_recognition@localhost",
                                        subject="AggregatedData",
                                        body=str(sensor_data.to_dict()))
                await self.send(msg_to_pattern)

    class AnalyzeDataBehaviour(PeriodicBehaviour):
        async def run(self):
            print("CentralCoordinator analyzing aggregated data")
            
            # In a real system, this would be more complex
            # For now, we'll just identify high activity zones based on recent data
            
            # Simple algorithm: if a location has > 5 cockroaches in last 3 readings
            high_activity_locations = {}
            
            for sensor_id, readings in self.agent.aggregated_data.items():
                if len(readings) >= 3:  # At least 3 readings
                    recent_count = sum([r.cockroach_count for r in readings[-3:]])
                    if recent_count > 5:
                        location = readings[-1].location
                        if location not in high_activity_locations:
                            high_activity_locations[location] = 0
                        high_activity_locations[location] += recent_count
            
            # Update high activity zones
            self.agent.high_activity_zones = [
                HighActivityZone(loc, count, datetime.now().isoformat())
                for loc, count in high_activity_locations.items()
            ]
            
            # Send high activity zones to NotificationService
            if self.agent.high_activity_zones:
                for zone in self.agent.high_activity_zones:
                    alert = AlertDetails(zone.location, zone.cockroach_count, zone.timestamp)
                    msg = Message(to="notification_service@localhost",
                                  subject="HighActivityZone",
                                  body=str(alert.to_dict()))
                    await self.send(msg)
                    
            print(f"CentralCoordinator identified high activity zones: {[z.location for z in self.agent.high_activity_zones]}")


class PatternRecognitionModuleAgent(agent.Agent):
    def __init__(self, jid, password):
        super().__init__(jid, password)

    async def setup(self):
        print("PatternRecognitionModuleAgent starting")
        
        # Add behaviour to receive aggregated data and analyze patterns
        analyse_behaviour = self.AnalyzePatternsBehaviour()
        self.add_behaviour(analyse_behaviour)

    class AnalyzePatternsBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg and msg.get_metadata("subject") == "AggregatedData":
                print("PatternRecognitionModule analyzing activity patterns")
                
                # In a real system, this would perform complex pattern recognition
                # For simulation, we'll just pass the data along
                
                # Send to CentralCoordinator (in a real system this would be more complex)
                msg_to_coordinator = Message(to="central_coordinator@localhost",
                                           subject="PatternAnalysisComplete",
                                           body=msg.body)
                await self.send(msg_to_coordinator)


class NotificationServiceAgent(agent.Agent):
    def __init__(self, jid, password):
        super().__init__(jid, password)

    async def setup(self):
        print("NotificationServiceAgent starting")
        
        # Add behaviour to receive high activity zone alerts
        receive_alert_behaviour = self.ReceiveAlertBehaviour()
        self.add_behaviour(receive_alert_behaviour)

    class ReceiveAlertBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg and msg.get_metadata("subject") == "HighActivityZone":
                print("NotificationService received high activity zone alert")
                
                # Parse alert details
                alert = AlertDetails.from_dict(eval(msg.body))
                
                # Send to Building Administration
                msg_to_admin = Message(to="building_administration@localhost",
                                      subject="Alert",
                                      body=str(alert.to_dict()))
                await self.send(msg_to_admin)
                
                # Send to Pest Control Company
                msg_to_pest = Message(to="pest_control_company@localhost",
                                     subject="Alert",
                                     body=str(alert.to_dict()))
                await self.send(msg_to_pest)
                
                # Send to Student Residents
                msg_to_students = Message(to="student_resident@localhost",
                                         subject="Alert",
                                         body=str(alert.to_dict()))
                await self.send(msg_to_students)
                
                print(f"NotificationService sent alerts for {alert.location}")


class BuildingAdministrationAgent(agent.Agent):
    def __init__(self, jid, password):
        super().__init__(jid, password)

    async def setup(self):
        print("BuildingAdministrationAgent starting")
        
        # Add behaviour to receive alerts
        receive_alert_behaviour = self.ReceiveAlertBehaviour()
        self.add_behaviour(receive_alert_behaviour)

    class ReceiveAlertBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg and msg.get_metadata("subject") == "Alert":
                print("BuildingAdministration received alert")
                
                # Parse alert details
                alert = AlertDetails.from_dict(eval(msg.body))
                
                print(f"Building Administration responding to alert at {alert.location}")
                
                # In a real system, this would trigger administrative actions
                # For simulation, we'll just log the response
                print(f"Building Administration: Alert responded to for {alert.location} with {alert.cockroach_count} cockroaches")


class PestControlCompanyAgent(agent.Agent):
    def __init__(self, jid, password):
        super().__init__(jid, password)

    async def setup(self):
        print("PestControlCompanyAgent starting")
        
        # Add behaviour to receive alerts
        receive_alert_behaviour = self.ReceiveAlertBehaviour()
        self.add_behaviour(receive_alert_behaviour)

    class ReceiveAlertBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg and msg.get_metadata("subject") == "Alert":
                print("PestControlCompany received alert")
                
                # Parse alert details
                alert = AlertDetails.from_dict(eval(msg.body))
                
                print(f"Pest Control Company responding to alert at {alert.location}")
                
                # In a real system, this would trigger treatment
                # For simulation, we'll just log the treatment
                print(f"Pest Control Company: Treatment executed at {alert.location} with {alert.cockroach_count} cockroaches")


class StudentResidentAgent(agent.Agent):
    def __init__(self, jid, password):
        super().__init__(jid, password)

    async def setup(self):
        print("StudentResidentAgent starting")
        
        # Add behaviour to receive notifications
        receive_notification_behaviour = self.ReceiveNotificationBehaviour()
        self.add_behaviour(receive_notification_behaviour)

    class ReceiveNotificationBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg and msg.get_metadata("subject") == "Alert":
                print("Student Resident received notification")
                
                # Parse alert details
                alert = AlertDetails.from_dict(eval(msg.body))
                
                print(f"Student Resident: Notification received for {alert.location} with {alert.cockroach_count} cockroaches")
                
                # In a real system, this would trigger user notification
                # For simulation, we'll just log
                print(f"Student Resident: Notification processed for {alert.location}")


def create_agents():
    agents = []
    
    # Create SensorNodeAgents
    for i in range(5):  # 5 sensor nodes
        agent_jid = f"sensor_node_{i}@localhost"
        agent_password = "password"
        location = f"Room_{random.randint(1, 100)}"
        sensor_agent = SensorNodeAgent(agent_jid, agent_password, f"sensor_{i}", location)
        agents.append(sensor_agent)
        
    # Create CentralCoordinatorAgent
    coordinator_agent = CentralCoordinatorAgent("central_coordinator@localhost", "password")
    agents.append(coordinator_agent)
    
    # Create PatternRecognitionModuleAgent
    pattern_agent = PatternRecognitionModuleAgent("pattern_recognition@localhost", "password")
    agents.append(pattern_agent)
    
    # Create NotificationServiceAgent
    notification_agent = NotificationServiceAgent("notification_service@localhost", "password")
    agents.append(notification_agent)
    
    # Create BuildingAdministrationAgent
    admin_agent = BuildingAdministrationAgent("building_administration@localhost", "password")
    agents.append(admin_agent)
    
    # Create PestControlCompanyAgent
    pest_agent = PestControlCompanyAgent("pest_control_company@localhost", "password")
    agents.append(pest_agent)
    
    # Create StudentResidentAgents
    for i in range(3):  # 3 student residents
        student_agent = StudentResidentAgent(f"student_resident_{i}@localhost", "password")
        agents.append(student_agent)
        
    return agents


async def run_system():
    print("Starting Multi-Agent System for Cockroach Detection...")
    
    agents = create_agents()
    
    # Start all agents
    for agent in agents:
        await agent.start()
        
    print("All agents started. System running for 60 seconds...")
    
    # Run for 60 seconds
    await asyncio.sleep(60)
    
    # Stop all agents
    for agent in agents:
        await agent.stop()
    
    print("System stopped.")

# Modified version to work with SPADE
if __name__ == "__main__":
    import asyncio
    
    # Create agents
    agents = create_agents()
    
    # Run agents in a simple way
    try:
        # Start all agents
        for agent in agents:
            asyncio.run(agent.start())
        
        print("All agents started. System running for 60 seconds...")
        
        # Run for 60 seconds
        asyncio.sleep(60)
        
        # Stop all agents
        for agent in agents:
            asyncio.run(agent.stop())
        
        print("System stopped.")
    except KeyboardInterrupt:
        print("System interrupted by user")
    except Exception as e:
        print(f"Error running system: {e}")