from typing import Dict, Any, List
from agents.base_agent import Agent


class ProtocolManager:
    """
    Manages communication protocols between agents
    """
    
    def __init__(self):
        self.protocols = {}
        self.agent_registry = {}
    
    def register_agent(self, agent: Agent):
        """Register an agent with the protocol manager"""
        self.agent_registry[agent.name] = agent
        
    def register_protocol(self, protocol_name: str, protocol_info: Dict[str, Any]):
        """Register a communication protocol"""
        self.protocols[protocol_name] = protocol_info
        
    def send_message(self, sender_name: str, receiver_name: str, protocol_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Send a message from one agent to another using a specific protocol"""
        
        # Get sender and receiver agents
        sender = self.agent_registry.get(sender_name)
        receiver = self.agent_registry.get(receiver_name)
        
        if not sender or not receiver:
            raise ValueError(f"Agent {sender_name} or {receiver_name} not found")
        
        # Validate protocol exists
        protocol = self.protocols.get(protocol_name)
        if not protocol:
            raise ValueError(f"Protocol {protocol_name} not found")
        
        # Process the message through the receiver
        result = receiver.process({protocol_name: data})
        
        return {
            'status': 'success',
            'sender': sender_name,
            'receiver': receiver_name,
            'protocol': protocol_name,
            'data': data,
            'result': result
        }
    
    def get_protocol_info(self, protocol_name: str) -> Dict[str, Any]:
        """Get information about a specific protocol"""
        return self.protocols.get(protocol_name, {})
    
    def list_protocols(self) -> List[str]:
        """List all registered protocols"""
        return list(self.protocols.keys())
    
    def list_agents(self) -> List[str]:
        """List all registered agents"""
        return list(self.agent_registry.keys())