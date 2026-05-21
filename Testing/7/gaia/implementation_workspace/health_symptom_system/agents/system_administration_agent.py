from agents.base_agent import BaseAgent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import json


class SystemAdministrationAgent(BaseAgent):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.system_metrics = {}
        self.logger.info(f"SystemAdministrationAgent {self.jid} initialized")

    async def setup(self):
        await super().setup()
        self.logger.info(f"SystemAdministrationAgent {self.jid} setup completed")

    async def initiate_system_monitoring(self):
        """Initiate system health monitoring"""
        try:
            # In a real system, this would collect actual system metrics
            # For demonstration, we'll simulate some metrics
            metrics = {
                "cpu_usage": 45.2,
                "memory_usage": 67.8,
                "disk_usage": 32.1,
                "active_agents": len(self.get_active_agents()),
                "timestamp": self.get_timestamp(),
                "monitoring_id": str(self.agent_id)
            }
            
            self.system_metrics = metrics
            self.logger.info(f"System metrics collected: {metrics}")
            
            # Send to MonitoringAgent
            msg = Message(to="monitoring_agent@localhost", 
                          body=json.dumps(metrics), 
                          subject="InitiateSystemMonitoring")
            await self.send(msg)
            self.logger.info("System metrics sent to MonitoringAgent")
            return metrics
        except Exception as e:
            self.logger.error(f"Error initiating system monitoring: {e}")
            return None

    def get_active_agents(self):
        # This would return list of active agents in a real system
        return ["user_agent", "llm_processor", "health_data_handler", "health_analyzer", "health_institution", "recommendation_engine"]

    def get_timestamp(self):
        from datetime import datetime
        return datetime.now().isoformat()

    async def handle_message(self, msg):
        """Handle incoming messages"""
        if msg.subject == "InitiateSystemMonitoring":
            await self.initiate_system_monitoring()
        else:
            self.logger.warning(f"Unknown message subject: {msg.subject}")
