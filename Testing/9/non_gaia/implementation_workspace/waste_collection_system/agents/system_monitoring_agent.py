from crewai import Agent
from pydantic import Field
from typing import Dict, List
from models.container import Container
from models.truck import Truck
from models.system import WasteCollectionSystem


class SystemMonitoringAgent:
    def __init__(self, system: WasteCollectionSystem):
        self.system = system
    
    def get_system_status(self) -> Dict:
        """Get overall system status report"""
        return {
            "total_containers": len(self.system.containers),
            "total_trucks": len(self.system.trucks),
            "full_containers": len(self.system.get_full_containers()),
            "warning_containers": len(self.system.get_warning_containers()),
            "overdue_containers": len(self.system.check_timely_removal()),
            "free_trucks": len(self.system.get_free_trucks()),
            "busy_trucks": len(self.system.get_busy_trucks()),
            "full_trucks": len(self.system.get_full_trucks())
        }
    
    def get_detailed_report(self) -> Dict:
        """Generate a detailed report of system status"""
        report = self.get_system_status()
        
        # Add detailed information
        report["containers"] = [
            {
                "id": container.id,
                "location": container.location,
                "fill_level": container.current_fill_level,
                "capacity": container.capacity,
                "status": container.status
            }
            for container in self.system.containers.values()
        ]
        
        report["trucks"] = [
            {
                "id": truck.id,
                "location": truck.location,
                "load": truck.current_load,
                "capacity": truck.capacity,
                "status": truck.status
            }
            for truck in self.system.trucks.values()
        ]
        
        return report
    
    def identify_bottlenecks(self) -> List[str]:
        """Identify potential bottlenecks in the system"""
        bottlenecks = []
        
        # Check for too many full containers
        full_containers = self.system.get_full_containers()
        if len(full_containers) > 0.5 * len(self.system.containers):
            bottlenecks.append("Too many full containers")
        
        # Check for too many full trucks
        full_trucks = self.system.get_full_trucks()
        if len(full_trucks) > 0.3 * len(self.system.trucks):
            bottlenecks.append("Too many full trucks")
        
        # Check for overdue containers
        overdue = self.system.check_timely_removal()
        if len(overdue) > 0:
            bottlenecks.append("Overdue containers")
        
        return bottlenecks