import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour
from spade.message import Message
from spade.template import Template
import json
import random
from datetime import datetime, timedelta
import logging


class CollectorAgent(Agent):
    def __init__(self, jid, password, position):
        super().__init__(jid, password)
        self.position = position  # (x, y) coordinates
        self.status = "available"  # available, busy, full
        self.container_capacity = 100  # percentage
        self.current_load = 0  # percentage
        self.max_load = 80  # percentage
        self.log_file = "collector_agent.log"
        
        # Setup logging
        self.logger = logging.getLogger(f"CollectorAgent-{self.jid}")
        handler = logging.FileHandler(self.log_file)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    async def setup(self):
        self.logger.info(f"Collector Agent {self.jid} starting with position {self.position}")
        
        # Add behaviours
        self.add_behaviour(self.AwaitPositionRequestBehaviour())
        self.add_behaviour(self.SendCollectorPositionBehaviour())
        self.add_behaviour(self.DispatchGarbageCollectorBehaviour())
        self.add_behaviour(self.EmptyContainerBehaviour())
        self.add_behaviour(self.SendEmptyConfirmationBehaviour())

    class AwaitPositionRequestBehaviour(CyclicBehaviour):
        async def run(self):
            # Wait for position request
            msg = await self.receive(timeout=10)
            if msg and msg.get_metadata("performative") == "request":
                self.agent.logger.info(f"Received position request from {msg.sender}")
                # Send position back
                response = Message(to=msg.sender, 
                                 body=json.dumps({"position": self.agent.position}),
                                 metadata={"performative": "inform"})
                await self.send(response)
                self.agent.logger.info(f"Sent position {self.agent.position} to {msg.sender}")

    class SendCollectorPositionBehaviour(PeriodicBehaviour):
        async def run(self):
            # Periodically send position
            self.agent.logger.info(f"Sending position {self.agent.position}")
            # In a real system, this would be done via a timer or event
            await asyncio.sleep(10)
            
    class DispatchGarbageCollectorBehaviour(CyclicBehaviour):
        async def run(self):
            # Wait for dispatch instructions
            msg = await self.receive(timeout=10)
            if msg and msg.get_metadata("performative") == "inform":
                self.agent.logger.info(f"Received dispatch instruction from {msg.sender}")
                # Parse the container position
                try:
                    container_data = json.loads(msg.body)
                    container_position = container_data["container_position"]
                    self.agent.logger.info(f"Dispatched to container at {container_position}")
                    
                    # Update status
                    self.agent.status = "busy"
                    
                    # Send confirmation back to dispatcher
                    response = Message(to=msg.sender,
                                     body=json.dumps({"status": "dispatched", "collector": str(self.agent.jid)}),
                                     metadata={"performative": "inform"})
                    await self.send(response)
                except Exception as e:
                    self.agent.logger.error(f"Error processing dispatch instruction: {e}")

    class EmptyContainerBehaviour(CyclicBehaviour):
        async def run(self):
            # Wait for empty container instruction
            msg = await self.receive(timeout=10)
            if msg and msg.get_metadata("performative") == "inform":
                self.agent.logger.info(f"Emptying container")
                # Simulate emptying process
                await asyncio.sleep(3)
                
                # Update load
                self.agent.current_load = max(0, self.agent.current_load - 20)
                
                # Send confirmation
                response = Message(to=msg.sender,
                                 body=json.dumps({"status": "container_empty", "collector": str(self.agent.jid)}),
                                 metadata={"performative": "inform"})
                await self.send(response)
                self.agent.logger.info(f"Container emptied")

    class SendEmptyConfirmationBehaviour(CyclicBehaviour):
        async def run(self):
            # Wait for confirmation request
            msg = await self.receive(timeout=10)
            if msg and msg.get_metadata("performative") == "request":
                self.agent.logger.info(f"Sending empty confirmation to {msg.sender}")
                # Send confirmation
                response = Message(to=msg.sender,
                                 body=json.dumps({"status": "confirmed", "collector": str(self.agent.jid)}),
                                 metadata={"performative": "inform"})
                await self.send(response)
