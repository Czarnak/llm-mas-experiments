from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from typing import Dict, Any, List
from mas_system.utils.logger import log_agent_action


class BaseAgent(Agent):
    """
    Base class for all agents in the Multi-Agent System
    """
    
    def __init__(self, jid: str, password: str, agent_name: str):
        super().__init__(jid, password)
        self.agent_name = agent_name
        self.protocols = {}
        self.logger = log_agent_action
        
    async def setup(self):
        await super().setup()
        print(f"{self.agent_name} agent started")
        
    def add_protocol(self, protocol_name: str, protocol):
        """
        Add a protocol to this agent
        """
        self.protocols[protocol_name] = protocol
        
    def get_protocol(self, protocol_name: str):
        """
        Get a protocol by name
        """
        return self.protocols.get(protocol_name)
        
    def send_message(self, to: str, content: Dict[str, Any], protocol: str = None):
        """
        Send a message to another agent
        """
        msg = Message(to=to, body=str(content))
        if protocol:
            msg.set_metadata("protocol", protocol)
        self.logger(self.agent_name, f"Sending message to {to}", str(content))
        return msg