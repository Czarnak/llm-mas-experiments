import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour
from spade.message import Message
from spade.template import Template
import json
import random
from datetime import datetime, timedelta
import logging


class CommunicatorAgent(Agent):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.collector_positions = {}
        self.container_positions = {}
        self.log_file = "communicator_agent.log"
        
        # Setup logging
        self.logger = logging.getLogger(f"CommunicatorAgent-{self.jid}")
        handler = logging.FileHandler(self.log_file)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    async def setup(self):
        self.logger.info(f"Communicator Agent {self.jid} starting")
        
        # Add behaviours
        self.add_behaviour(self.RequestCollectorPositionBehaviour())
        self.add_behaviour(self.GetContainerFullBehaviour())
        self.add_behaviour(self.FindBestGarbageTruckBehaviour())
        self.add_behaviour(self.DispatchGarbageCollectorBehaviour())
        self.add_behaviour(self.SendCollectorPositionBehaviour())

    class RequestCollectorPositionBehaviour(CyclicBehaviour):
        async def run(self):
            # Request position from all collectors
            self.agent.logger.info(f"Requesting positions from collectors")
            
            # In a real system, this would be done via a broadcast or specific request
            # For now, we'll simulate with a fixed list
            collectors = ["collector1@localhost", "collector2@localhost", "collector3@localhost"]
            
            for collector in collectors:
                msg = Message(to=collector,
                             body=json.dumps({"request": "position"}),
                             metadata={"performative": "request"})
                await self.send(msg)
                self.agent.logger.info(f"Requested position from {collector}")
                
            # Wait for responses
            for i in range(len(collectors)):
                msg = await self.receive(timeout=5)
                if msg and msg.get_metadata("performative") == "inform":
                    try:
                        position_data = json.loads(msg.body)
                        self.agent.collector_positions[msg.sender] = position_data["position"]
                        self.agent.logger.info(f"Received position from {msg.sender}: {position_data['position']}")
                    except Exception as e:
                        self.agent.logger.error(f"Error processing position data from {msg.sender}: {e}")

    class GetContainerFullBehaviour(CyclicBehaviour):
        async def run(self):
            # Wait for container full notifications
            msg = await self.receive(timeout=10)
            if msg and msg.get_metadata("performative") == "inform":
                self.agent.logger.info(f"Received container full notification")
                try:
                    container_data = json.loads(msg.body)
                    container_position = container_data["container_position"]
                    
                    # Store container position
                    self.agent.container_positions[container_position] = {
                        "timestamp": datetime.now(),
                        "status": "full"
                    }
                    
                    self.agent.logger.info(f"Container at {container_position} marked as full")
                except Exception as e:
                    self.agent.logger.error(f"Error processing container full notification: {e}")

    class FindBestGarbageTruckBehaviour(CyclicBehaviour):
        async def run(self):
            # Wait for container full notification to find best truck
            msg = await self.receive(timeout=10)
            if msg and msg.get_metadata("performative") == "inform":
                self.agent.logger.info(f"Finding best garbage truck")
                
                # For now, just pick a random available collector
                # In a real system, this would calculate distances
                available_collectors = [jid for jid, pos in self.agent.collector_positions.items() 
                                      if self.agent.status != "busy"]
                
                if available_collectors:
                    best_collector = random.choice(available_collectors)
                    self.agent.logger.info(f"Selected {best_collector} as best collector")
                    
                    # Store the dispatch info
                    self.agent.dispatch_info = {
                        "collector": best_collector,
                        "container": msg.body
                    }
                else:
                    self.agent.logger.warning("No available collectors")

    class DispatchGarbageCollectorBehaviour(CyclicBehaviour):
        async def run(self):
            # Wait for dispatch instructions
            msg = await self.receive(timeout=10)
            if msg and msg.get_metadata("performative") == "inform":
                self.agent.logger.info(f"Dispatching collector")
                
                # Send dispatch instruction to collector
                try:
                    collector_jid = self.agent.dispatch_info["collector"]
                    container_position = self.agent.dispatch_info["container"]
                    
                    dispatch_msg = Message(to=collector_jid,
                                         body=json.dumps({"container_position": container_position}),
                                         metadata={"performative": "inform"})
                    await self.send(dispatch_msg)
                    self.agent.logger.info(f"Dispatched {collector_jid} to container at {container_position}")
                except Exception as e:
                    self.agent.logger.error(f"Error dispatching collector: {e}")

    class SendCollectorPositionBehaviour(PeriodicBehaviour):
        async def run(self):
            # Periodically send collector positions
            self.agent.logger.info(f"Sending collector positions")
            await asyncio.sleep(10)
            # This would be used for monitoring purposes
