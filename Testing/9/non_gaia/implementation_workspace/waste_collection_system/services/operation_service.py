from models.system import WasteCollectionSystem
from agents.container_monitoring_agent import ContainerMonitoringAgent
from agents.truck_management_agent import TruckManagementAgent
from agents.task_assignment_agent import TaskAssignmentAgent
from agents.system_monitoring_agent import SystemMonitoringAgent
from typing import List, Dict


class OperationService:
    def __init__(self, system: WasteCollectionSystem):
        self.system = system
        self.container_monitor = ContainerMonitoringAgent(system)
        self.truck_manager = TruckManagementAgent(system)
        self.task_assigner = TaskAssignmentAgent(system)
        self.system_monitor = SystemMonitoringAgent(system)
    
    def initialize_system(self):
        """Initialize the system with some sample data"""
        from models.container import Container
        from models.truck import Truck
        
        # Add sample containers
        if "C001" not in self.system.containers:
            container1 = self.system.add_container(
                Container(
                    id="C001",
                    location="Location A",
                    capacity=1000,
                    current_fill_level=950
                )
            )
        
        if "C002" not in self.system.containers:
            container2 = self.system.add_container(
                Container(
                    id="C002",
                    location="Location B",
                    capacity=1000,
                    current_fill_level=800
                )
            )
        
        if "C003" not in self.system.containers:
            container3 = self.system.add_container(
                Container(
                    id="C003",
                    location="Location C",
                    capacity=1000,
                    current_fill_level=900
                )
            )
        
        # Add sample trucks
        if "T001" not in self.system.trucks:
            truck1 = self.system.add_truck(
                Truck(
                    id="T001",
                    location="Depot A",
                    capacity=2000,
                    current_load=0
                )
            )
        
        if "T002" not in self.system.trucks:
            truck2 = self.system.add_truck(
                Truck(
                    id="T002",
                    location="Depot B",
                    capacity=2000,
                    current_load=0
                )
            )
    
    def run_system_check(self):
        """Run a complete system check and return status"""
        print("=== SYSTEM STATUS CHECK ===")
        status = self.system_monitor.get_system_status()
        for key, value in status.items():
            print(f"{key}: {value}")
        
        print("\n=== CONTAINERS STATUS ===")
        containers = self.system.containers.values()
        for container in containers:
            print(f"Container {container.id}: {container.status} (Fill: {container.current_fill_level}/{container.capacity})")
        
        print("\n=== TRUCKS STATUS ===")
        trucks = self.system.trucks.values()
        for truck in trucks:
            print(f"Truck {truck.id}: {truck.status} (Load: {truck.current_load}/{truck.capacity})")
        
        return status
    
    def process_overdue_containers(self):
        """Process containers that haven't been emptied in more than 1 day"""
        overdue = self.system.check_timely_removal()
        print(f"\n=== OVERDUE CONTAINERS ({len(overdue)}) ===")
        for container_id in overdue:
            print(f"Container {container_id} is overdue for emptying")
            
        # Assign trucks to overdue containers
        for container_id in overdue:
            truck_id = self.task_assigner.assign_truck_to_container(container_id)
            if truck_id:
                print(f"Assigned truck {truck_id} to overdue container {container_id}")
            else:
                print(f"No available trucks for container {container_id}")
    
    def process_full_containers(self):
        """Process containers that are full or at warning level"""
        full_containers = self.system.get_full_containers()
        warning_containers = self.system.get_warning_containers()
        
        print(f"\n=== FULL CONTAINERS ({len(full_containers)}) ===")
        for container in full_containers:
            print(f"Container {container.id}: {container.status} (Fill: {container.current_fill_level}/{container.capacity})")
        
        print(f"\n=== WARNING CONTAINERS ({len(warning_containers)}) ===")
        for container in warning_containers:
            print(f"Container {container.id}: {container.status} (Fill: {container.current_fill_level}/{container.capacity})")
        
        # Assign trucks to full containers
        for container in full_containers:
            truck_id = self.task_assigner.assign_truck_to_container(container.id)
            if truck_id:
                print(f"Assigned truck {truck_id} to full container {container.id}")
            else:
                print(f"No available trucks for container {container.id}")
        
        # Assign trucks to warning containers
        for container in warning_containers:
            truck_id = self.task_assigner.assign_truck_to_container(container.id)
            if truck_id:
                print(f"Assigned truck {truck_id} to warning container {container.id}")
            else:
                print(f"No available trucks for container {container.id}")
    
    def prioritize_and_assign_trucks(self):
        """Prioritize trucks and assign tasks based on priority"""
        print("\n=== PRIORITIZING TRUCKS ===")
        prioritized_trucks = self.truck_manager.prioritize_trucks()
        for i, truck in enumerate(prioritized_trucks):
            print(f"Priority {i+1}: Truck {truck.id} (Load: {truck.current_load}/{truck.capacity})")
        
        # Assign tasks to trucks that are full
        full_trucks = self.system.get_full_trucks()
        for truck in full_trucks:
            print(f"Truck {truck.id} is full, needs to be emptied")
            # In a real system, this would trigger a return to depot or another action
    
    def run_simulation(self):
        """Run a complete simulation of the waste collection system"""
        print("Starting Waste Collection System Simulation")
        
        # Initialize system with sample data
        self.initialize_system()
        
        # Run system check
        self.run_system_check()
        
        # Process overdue containers
        self.process_overdue_containers()
        
        # Process full containers
        self.process_full_containers()
        
        # Prioritize and assign trucks
        self.prioritize_and_assign_trucks()
        
        # Final system check
        print("\n=== FINAL SYSTEM STATUS ===")
        self.run_system_check()
        
        return self.system_monitor.get_detailed_report()