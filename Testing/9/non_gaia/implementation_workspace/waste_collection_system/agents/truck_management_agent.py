from crewai import Agent
from pydantic import Field
from typing import List, Optional
from models.truck import Truck
from models.system import WasteCollectionSystem


class TruckManagementAgent:
    def __init__(self, system: WasteCollectionSystem):
        self.system = system
    
    def get_truck_status(self, truck_id: str) -> Truck:
        """Get detailed status of a specific truck"""
        return self.system.get_truck_by_id(truck_id)
    
    def update_truck_status(self, truck_id: str, new_status: str):
        """Update the status of a truck"""
        truck = self.system.get_truck_by_id(truck_id)
        if truck:
            truck.status = new_status
            return True
        return False
    
    def get_available_trucks(self) -> List[Truck]:
        """Get all trucks that are currently free"""
        return self.system.get_free_trucks()
    
    def get_full_trucks(self) -> List[Truck]:
        """Get all trucks that are full"""
        return self.system.get_full_trucks()
    
    def prioritize_trucks(self) -> List[Truck]:
        """Get trucks prioritized by fill level"""
        return self.system.prioritize_trucks()
