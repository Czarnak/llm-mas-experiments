import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour
from spade.message import Message
from spade.template import Template
import json
import random
from datetime import datetime, timedelta
import logging


class ContainerAgent(Agent):
    def __init__(self, jid, password, position, capacity=100):
        super().__init__(jid, password)
        self.position = position  # (x, y) coordinates
        self.capacity = capacity  # percentage
        self.current_fill = 0  # percentage
        self.full_threshold = 80  # percentage
        self.log_file = "container_agent.log"
        self.last_empty_time = datetime.now()
        
        # Setup logging
        self.logger = logging.getLogger(f"ContainerAgent-{self.jid}")
        handler = logging.FileHandler(self.log_file)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    async def setup(self):
        self.logger.info(f"Container Agent {self.jid} starting at position {self.position}")
        
        # Add behaviours
        self.add_behaviour(self.GetGarbageLevelBehaviour())
        self.add_behaviour(self.SendContainerFullBehaviour())
        self.add_behaviour(self.GetEmptyConfirmationBehaviour())
        self.add_behaviour(self.ContainerMonitorBehaviour())

    class GetGarbageLevelBehaviour(CyclicBehaviour):
        async def run(self):
            # Simulate garbage level monitoring
            await asyncio.sleep(2)
            
            # Simulate increasing fill level
            self.agent.current_fill = min(100, self.agent.current_fill + random.randint(1, 5))
            
            self.agent.logger.info(f"Current fill level {self.agent.current_fill}%")
            
            # Check if container is full
            if self.agent.current_fill >= self.agent.full_threshold:
                self.agent.logger.info(f"Container is full")
                
                # Send notification to communicator
                msg = Message(to="communicator@localhost",
                             body=json.dumps({"container_position": self.agent.position}),
                             metadata={"performative": "inform"})
                await self.send(msg)
                self.agent.logger.info(f"Sent full notification")

    class SendContainerFullBehaviour(CyclicBehaviour):
        async def run(self):
            # Wait for container full notification
            msg = await self.receive(timeout=10)
            if msg and msg.get_metadata("performative") == "inform":
                self.agent.logger.info(f"Sending full notification")
                # In a real system, this would be triggered by the GetGarbageLevelBehaviour
                # For now, we'll simulate it
                pass

    class GetEmptyConfirmationBehaviour(CyclicBehaviour):
        async def run(self):
            # Wait for empty confirmation
            msg = await self.receive(timeout=10)
            if msg and msg.get_metadata("performative") == "inform":
                self.agent.logger.info(f"Received empty confirmation")
                # Reset fill level
                self.agent.current_fill = 0
                self.agent.last_empty_time = datetime.now()
                self.agent.logger.info(f"Container reset")

    class ContainerMonitorBehaviour(PeriodicBehaviour):
        async def run(self):
            # Periodically check container status
            self.agent.logger.info(f"Monitoring container status")
            
            # Check if container has been full for too long (1 day)
            time_since_full = datetime.now() - self.agent.last_empty_time
            if time_since_full > timedelta(days=1):
                self.agent.logger.warning(f"Container has been full for more than 1 day!")
                # This could trigger an emergency response
