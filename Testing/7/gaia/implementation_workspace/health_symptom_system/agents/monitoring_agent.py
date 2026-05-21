from agents.base_agent import BaseAgent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import json


class MonitoringAgent(BaseAgent):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.monitoring_reports = []
        self.logger.info(f"MonitoringAgent {self.jid} initialized")

    async def setup(self):
        await super().setup()
        self.logger.info(f"MonitoringAgent {self.jid} setup completed")

    async def receive_system_metrics(self, metrics):
        """Receive and process system metrics"""
        try:
            report = {
                "metrics": metrics,
                "timestamp": self.get_timestamp(),
                "report_id": str(self.agent_id)
            }
            
            self.monitoring_reports.append(report)
            self.logger.info(f"System metrics report received: {report}")
            
            # In a real system, this would log to monitoring system or trigger alerts
            return report
        except Exception as e:
            self.logger.error(f"Error receiving system metrics: {e}")
            return None

    def get_timestamp(self):
        from datetime import datetime
        return datetime.now().isoformat()

    async def handle_message(self, msg):
        """Handle incoming messages"""
        if msg.subject == "InitiateSystemMonitoring":
            await self.receive_system_metrics(json.loads(msg.body))
        else:
            self.logger.warning(f"Unknown message subject: {msg.subject}")
