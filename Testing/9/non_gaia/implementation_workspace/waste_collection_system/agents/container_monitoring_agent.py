from crewai import Agent
from pydantic import Field
from typing import List
from models.container import Container
from models.system import WasteCollectionSystem


class ContainerMonitoringAgent:
    def __init__(self, system: WasteCollectionSystem):
        self.system = system
        
    def check_container_status(self) -> List[str]:
        """Check all containers and return IDs of those that need attention"""
        full_containers = self.system.get_full_containers()
        warning_containers = self.system.get_warning_containers()
        overdue_containers = self.system.check_timely_removal()
        
        containers_needing_attention = []
        
        for container in full_containers:
            containers_needing_attention.append(container.id)
            
        for container in warning_containers:
            containers_needing_attention.append(container.id)
            
        for container_id in overdue_containers:
            containers_needing_attention.append(container_id)
            
        return containers_needing_attention
    
    def get_container_info(self, container_id: str) -> Container:
        """Get detailed information about a specific container"""
        return self.system.get_container_by_id(container_id)
