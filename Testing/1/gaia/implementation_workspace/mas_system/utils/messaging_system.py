from typing import Dict, List, Optional, Any
from typing import Dict, List, Optional
from ..agents.base_agent import AgentMessage, BaseAgent


class MessagingSystem:
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        
    def register_agent(self, agent: BaseAgent):
        self.agents[agent.agent_id] = agent
        
    def send_message(self, sender_id: str, receiver_id: str, protocol: str, content: Dict[str, Any]) -> Optional[AgentMessage]:
        sender = self.agents.get(sender_id)
        receiver = self.agents.get(receiver_id)
        
        if not sender or not receiver:
            return None
        
        # Create and send message
        message = sender.send_message(receiver_id, protocol, content)
        
        # Add to receiver's queue
        receiver.add_to_queue(message)
        
        # Process the message immediately
        return receiver.process_message(message)
    
    def process_all_queues(self):
        for agent in self.agents.values():
            agent.process_queue()
    
    def get_agent(self, agent_id: str) -> Optional[BaseAgent]:
        return self.agents.get(agent_id)
    
    def get_all_agents(self) -> Dict[str, BaseAgent]:
        return self.agents