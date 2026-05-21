import asyncio
from spade import agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from datetime import datetime, timedelta
import random
import json

# Agent classes

class ContainerAgent(agent.Agent):
    def __init__(self, jid, password, container_id, fill_level=0):
        super().__init__(jid, password)
        self.container_id = container_id
        self.fill_level = fill_level
        self.timestamp = datetime.now()
        
    async def setup(self):
        print(f"ContainerAgent {self.container_id} starting...")
        
        # Add behaviour to periodically update fill level and send notifications
        self.add_behaviour(self.ContainerBehaviour())
        
    class ContainerBehaviour(CyclicBehaviour):
        async def run(self):
            # Simulate container fill level increasing over time
            self.agent.fill_level += random.randint(1, 5)
            if self.agent.fill_level > 100:
                self.agent.fill_level = 100
                
            self.agent.timestamp = datetime.now()
            
            # Check if container needs emptying
            if self.agent.fill_level >= 90:
                # Send notification to dispatch system
                msg = Message(to="dispatch_system@localhost", 
                              subject="ContainerToDispatchSystemNotification",
                              body=json.dumps({
                                  "ContainerID": self.agent.container_id,
                                  "FillLevel": self.agent.fill_level,
                                  "Timestamp": self.agent.timestamp.isoformat()
                              }))
                await self.send(msg)
                print(f"Container {self.agent.container_id} sent notification - Fill Level: {self.agent.fill_level}%")
                
            await asyncio.sleep(5)


class GarbageTruckAgent(agent.Agent):
    def __init__(self, jid, password, truck_id, status="Available", fill_level=0):
        super().__init__(jid, password)
        self.truck_id = truck_id
        self.status = status  # Available, Busy, Maintenance
        self.fill_level = fill_level
        self.timestamp = datetime.now()
        
    async def setup(self):
        print(f"GarbageTruckAgent {self.truck_id} starting...")
        
        # Add behaviour to handle assignments
        self.add_behaviour(self.GarbageTruckBehaviour())
        
    class GarbageTruckBehaviour(CyclicBehaviour):
        async def run(self):
            # Check for incoming messages
            msg = await self.receive(timeout=1)
            if msg and msg.subject == "DispatchSystemToGarbageTruckAssignment":
                assignment_data = json.loads(msg.body)
                print(f"Garbage Truck {self.agent.truck_id} received assignment for container {assignment_data['ContainerID']}")
                
                # Update status to Busy
                self.agent.status = "Busy"
                self.agent.timestamp = datetime.now()
                
                # Simulate collection process
                await asyncio.sleep(3)
                
                # Update status back to Available
                self.agent.status = "Available"
                self.agent.timestamp = datetime.now()
                print(f"Garbage Truck {self.agent.truck_id} completed assignment")
                
            await asyncio.sleep(1)


class DispatchSystemAgent(agent.Agent):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.containers = {}
        self.trucks = {}
        self.assignments = {}
        
    async def setup(self):
        print("DispatchSystemAgent starting...")
        
        # Add behaviours for different responsibilities
        self.add_behaviour(self.DispatchSystemBehaviour())
        self.add_behaviour(self.ContainerStatusMonitor())
        self.add_behaviour(self.GarbageTruckStatusMonitor())
        
    class DispatchSystemBehaviour(CyclicBehaviour):
        async def run(self):
            # Check for incoming messages
            msg = await self.receive(timeout=1)
            if msg and msg.subject == "ContainerToDispatchSystemNotification":
                notification_data = json.loads(msg.body)
                container_id = notification_data["ContainerID"]
                fill_level = notification_data["FillLevel"]
                
                print(f"Dispatch System received notification from container {container_id} - Fill Level: {fill_level}%")
                
                # Store container data
                self.agent.containers[container_id] = {
                    "FillLevel": fill_level,
                    "Timestamp": notification_data["Timestamp"],
                    "Deadline": (datetime.now() + timedelta(days=1)).isoformat()
                }
                
                # Find nearest available truck
                nearest_truck = self.find_nearest_available_truck()
                if nearest_truck:
                    # Assign truck to container
                    self.agent.assignments[container_id] = nearest_truck
                    
                    # Send assignment to truck
                    msg = Message(to=f"{nearest_truck}@localhost", 
                                  subject="DispatchSystemToGarbageTruckAssignment",
                                  body=json.dumps({
                                      "ContainerID": container_id,
                                      "GarbageTruckID": nearest_truck,
                                      "EstimatedArrivalTime": datetime.now().isoformat()
                                  }))
                    await self.send(msg)
                    print(f"Dispatch System assigned truck {nearest_truck} to container {container_id}")
                
            await asyncio.sleep(1)
            
        def find_nearest_available_truck(self):
            # Simple logic: find first available truck
            for truck_id, truck_data in self.agent.trucks.items():
                if truck_data["Status"] == "Available":
                    return truck_id
            return None
            
    class ContainerStatusMonitor(CyclicBehaviour):
        async def run(self):
            # Monitor container statuses (in a real system, this would be a periodic check)
            await asyncio.sleep(5)
            
    class GarbageTruckStatusMonitor(CyclicBehaviour):
        async def run(self):
            # Monitor garbage truck statuses (in a real system, this would be a periodic check)
            await asyncio.sleep(5)


async def main():
    print("Starting Multi-Agent Waste Management System...")
    
    # Create agents with proper JIDs and passwords
    container1 = ContainerAgent("container1@localhost", "password1", "C001", 85)
    container2 = ContainerAgent("container2@localhost", "password2", "C002", 70)
    container3 = ContainerAgent("container3@localhost", "password3", "C003", 60)
    
    truck1 = GarbageTruckAgent("truck1@localhost", "password4", "T001", "Available", 0)
    truck2 = GarbageTruckAgent("truck2@localhost", "password5", "T002", "Available", 0)
    
    dispatch_system = DispatchSystemAgent("dispatch_system@localhost", "password6")
    
    # Start agents
    await container1.start()
    await container2.start()
    await container3.start()
    await truck1.start()
    await truck2.start()
    await dispatch_system.start()
    
    # Register trucks in dispatch system
    dispatch_system.trucks["T001"] = {"Status": "Available", "FillLevel": 0}
    dispatch_system.trucks["T002"] = {"Status": "Available", "FillLevel": 0}
    
    print("System initialized. Running simulation for 30 seconds...")
    
    # Run for 30 seconds
    await asyncio.sleep(30)
    
    # Stop agents
    await container1.stop()
    await container2.stop()
    await container3.stop()
    await truck1.stop()
    await truck2.stop()
    await dispatch_system.stop()
    
    print("Simulation completed.")

if __name__ == "__main__":
    asyncio.run(main())