from typing import Dict, Any, List
from pydantic import BaseModel


class ServiceManager:
    """
    Manages services provided by agents
    """
    
    def __init__(self):
        self.services = {}
        self.agent_services = {}
    
    def register_service(self, service_name: str, service_info: Dict[str, Any]):
        """Register a service provided by an agent"""
        self.services[service_name] = service_info
        
    def get_service(self, service_name: str) -> Dict[str, Any]:
        """Get information about a specific service"""
        return self.services.get(service_name, {})
    
    def list_services(self) -> List[str]:
        """List all registered services"""
        return list(self.services.keys())
    
    def get_service_provider(self, service_name: str) -> str:
        """Get the agent that provides a specific service"""
        service_info = self.services.get(service_name)
        return service_info.get('provided_by') if service_info else None
    
    def register_agent_service(self, agent_name: str, service_name: str):
        """Register that an agent provides a specific service"""
        if agent_name not in self.agent_services:
            self.agent_services[agent_name] = []
        self.agent_services[agent_name].append(service_name)
    
    def get_agent_services(self, agent_name: str) -> List[str]:
        """Get all services provided by an agent"""
        return self.agent_services.get(agent_name, [])