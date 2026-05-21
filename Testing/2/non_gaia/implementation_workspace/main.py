from crewai import Crew, Agent, Task
from agents.sensor_agent import SensorAgent
from agents.coordinator_agent import CoordinatorAgent
from agents.alerting_agent import AlertingAgent
from agents.notification_agent import NotificationAgent
from utils.data_models import SensorData
from datetime import datetime
import time
import random


class RatDetectionSystem:
    def __init__(self):
        # Initialize agents
        self.sensor1 = SensorAgent(sensor_id='sensor_001', location='Building A, Room 101')
        self.sensor2 = SensorAgent(sensor_id='sensor_002', location='Building A, Room 102')
        self.sensor3 = SensorAgent(sensor_id='sensor_003', location='Building A, Room 103')
        
        self.coordinator = CoordinatorAgent()
        self.alerting = AlertingAgent()
        self.notification = NotificationAgent()
        
        # Create a simple crew to manage the workflow
        self.crew = Crew(
            agents=[self.sensor1, self.coordinator, self.alerting, self.notification],
            tasks=[],  # Tasks will be defined dynamically
            verbose=True
        )
    
    def generate_sensor_data(self):
        '''Generate data from sensors'''
        sensors = [self.sensor1, self.sensor2, self.sensor3]
        data_list = []
        
        for sensor in sensors:
            data = sensor.generate_data()
            data_list.append(data)
            print(f"Sensor {sensor.sensor_id} generated data: {data}")
        
        return data_list
    
    def process_data(self, data_list):
        '''Process data through coordinator'''
        for data in data_list:
            # Coordinator receives and processes data
            processed_data = self.coordinator.receive_data(data)
            
            # Check if we should generate an alert
            if processed_data.rat_count > 0:
                alert = self.coordinator.generate_alert(processed_data.location, processed_data.rat_count)
                self.alerting.send_alert(alert)
                
                # Update room status for notification
                if 'Room' in processed_data.location:
                    room_id = processed_data.location.split('Room ')[-1]
                    if processed_data.rat_count >= 5:
                        status = 'warning'
                        message = f'Rat activity detected in room {room_id}. Please be cautious.'
                    else:
                        status = 'safe'
                        message = f'No significant rat activity detected in room {room_id}.'
                    
                    self.notification.update_room_status(f'room_{room_id}', status, message)
    
    def run_simulation(self):
        '''Run the simulation for multiple time periods'''
        print("Starting Rat Detection and Alerting System")
        print("============================================")
        
        print("\nStarting simulation for 5 time periods...")
        
        for i in range(5):
            print(f"\n--- Time Period {i+1} ---")
            
            # Generate sensor data
            data_list = self.generate_sensor_data()
            
            # Process data
            self.process_data(data_list)
            
            # Wait before next time period
            time.sleep(1)
        
        # Show final analysis
        print("\n--- FINAL ANALYSIS ---")
        stats = self.coordinator.analyze_patterns()
        hotspots = self.coordinator.identify_hotspots()
        
        for location, stats_data in stats.items():
            print(f"{location}:")
            print(f"  Total Events: {stats_data['total_events']}")
            print(f"  Total Rats: {stats_data['total_rats']}")
            print(f"  Average Rats: {stats_data['avg_rats']:.2f}")
            print(f"  Max Rats: {stats_data['max_rats']}")
            
        if hotspots:
            print(f"\nHotspots identified: {', '.join(hotspots)}")
        else:
            print("\nNo significant hotspots identified.")
        
        print("\nSystem simulation completed.")


def main():
    system = RatDetectionSystem()
    system.run_simulation()


if __name__ == "__main__":
    main()