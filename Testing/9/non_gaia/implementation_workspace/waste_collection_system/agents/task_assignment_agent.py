from crewai import Agent
from pydantic import Field
from typing import Optional
from models.container import Container
from models.truck import Truck
from models.system import WasteCollectionSystem


class TaskAssignmentAgent:
    def __init__(self, system: WasteCollectionSystem):
        self.system = system
    
    def assign_truck_to_container(self, container_id: str) -> Optional[str]:
        """Assign the nearest available truck to a container that needs emptying"""
        container = self.system.get_container_by_id(container_id)
        if not container:
            return None
        
        # Check if container needs emptying
        if container.status in ["full", "warning"] or container.last_empty_time is None:
            # Find the nearest available truck
            truck = self.system.get_nearest_available_truck(container.location)
            if truck:
                # Assign the truck to the container
                truck.assign_container(container_id)
                container.update_fill_level(0)  # Reset container level
                return truck.id
        
        return None
    
    def get_pending_tasks(self) -> list:
        """Get all containers that need attention but haven't been assigned to trucks"""
        full_containers = self.system.get_full_containers()
        warning_containers = self.system.get_warning_containers()
        overdue_containers = self.system.check_timely_removal()
        
        pending_tasks = []
        
        for container in full_containers:
            if not container.last_empty_time:
                pending_tasks.append(container.id)
            
        for container in warning_containers:
            if not container.last_empty_time:
                pending_tasks.append(container.id)
            
        for container_id in overdue_containers:
            pending_tasks.append(container_id)
            
        return pending_tasks
