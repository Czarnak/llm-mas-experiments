from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime
from models.container import Container
from models.truck import Truck


class WasteCollectionSystem(BaseModel):
    containers: Dict[str, Container] = Field(default_factory=dict)
    trucks: Dict[str, Truck] = Field(default_factory=dict)
    
    def add_container(self, container: Container):
        """Add a container to the system"""
        self.containers[container.id] = container
    
    def add_truck(self, truck: Truck):
        """Add a truck to the system"""
        self.trucks[truck.id] = truck
    
    def get_full_containers(self) -> List[Container]:
        """Get all containers that are full"""
        return [container for container in self.containers.values() if container.status == "full"]
    
    def get_warning_containers(self) -> List[Container]:
        """Get all containers that are at warning level"""
        return [container for container in self.containers.values() if container.status == "warning"]
    
    def get_free_trucks(self) -> List[Truck]:
        """Get all trucks that are free"""
        return [truck for truck in self.trucks.values() if truck.status == "free"]
    
    def get_busy_trucks(self) -> List[Truck]:
        """Get all trucks that are busy"""
        return [truck for truck in self.trucks.values() if truck.status == "busy"]
    
    def get_full_trucks(self) -> List[Truck]:
        """Get all trucks that are full"""
        return [truck for truck in self.trucks.values() if truck.status == "full"]
    
    def get_truck_by_id(self, truck_id: str) -> Truck:
        """Get a truck by its ID"""
        return self.trucks.get(truck_id)
    
    def get_container_by_id(self, container_id: str) -> Container:
        """Get a container by its ID"""
        return self.containers.get(container_id)
    
    def get_nearest_available_truck(self, container_location: str) -> Optional[Truck]:
        """Find the nearest available truck for a container"""
        free_trucks = self.get_free_trucks()
        if not free_trucks:
            return None
        
        # Simple implementation - in a real system we'd calculate actual distances
        # For now, just return the first free truck
        return free_trucks[0]
    
    def check_timely_removal(self) -> List[str]:
        """Check for containers that haven't been emptied in more than 1 day"""
        from datetime import timedelta
        
        overdue_containers = []
        now = datetime.now()
        
        for container in self.containers.values():
            if container.last_empty_time:
                time_since_empty = now - container.last_empty_time
                if time_since_empty > timedelta(days=1):
                    overdue_containers.append(container.id)
        
        return overdue_containers
    
    def prioritize_trucks(self) -> List[Truck]:
        """Prioritize trucks based on fill level (more filled trucks first)"""
        # Sort trucks by current load percentage (descending)
        sorted_trucks = sorted(self.trucks.values(), key=lambda truck: truck.current_load / truck.capacity, reverse=True)
        return sorted_trucks
