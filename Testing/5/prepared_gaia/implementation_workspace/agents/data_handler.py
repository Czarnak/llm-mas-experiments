import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour
from spade.message import Message
from spade.template import Template
from datetime import datetime
import uuid

from core.message_types import Request, AvailableMaterials, MatchInformation
from core.database import Database
from utils.logger import get_logger


class DataHandlerAgent(Agent):
    def __init__(self, jid: str, password: str, db_path: str = "crisis_transport.db"):
        super().__init__(jid, password)
        self.db_path = db_path
        self.db = Database(db_path)
        self.logger = get_logger("DataHandlerAgent")
        
    async def setup(self):
        self.logger.info(f"Starting DataHandlerAgent: {self.jid}")
        
        # Initialize database
        await self.db.init_db()
        
        # Add the behaviour to await requests
        self.add_behaviour(self.AwaitRequestBehaviour())
        
        # Add the behaviour to await match information
        self.add_behaviour(self.AwaitMatchInformationBehaviour())
        
        # Add the behaviour to produce available materials
        self.add_behaviour(self.ProduceAvailableMaterialsBehaviour())
        
    class AwaitRequestBehaviour(CyclicBehaviour):
        async def run(self):
            # Listen for incoming requests
            template = Template()
            template.subject = "Request"
            
            msg = await self.receive(template)
            if msg:
                self.agent.logger.info(f"Received request: {msg.body}")
                
                # Parse request
                request_dict = eval(msg.body)
                request = Request(
                    id=request_dict["id"],
                    requester_id=request_dict["requester_id"],
                    resource_type=request_dict["resource_type"],
                    quantity=request_dict["quantity"],
                    location=request_dict["location"],
                    timestamp=datetime.fromisoformat(request_dict["timestamp"]),
                    status=request_dict["status"]
                )
                
                # Store in database
                await self.agent.db.add_request(request)
                
                # Notify the requester that request was received
                response_msg = Message(
                    to=msg.sender,
                    body=f"Request {request.id} received and stored",
                    subject="RequestReceived"
                )
                await self.send(response_msg)
                
    class AwaitMatchInformationBehaviour(CyclicBehaviour):
        async def run(self):
            # Listen for match information
            template = Template()
            template.subject = "MatchInformation"
            
            msg = await self.receive(template)
            if msg:
                self.agent.logger.info(f"Received match information: {msg.body}")
                
                # Parse match information
                match_dict = eval(msg.body)
                match = MatchInformation(
                    id=match_dict["id"],
                    request_id=match_dict["request_id"],
                    available_materials_id=match_dict["available_materials_id"],
                    matched_quantity=match_dict["matched_quantity"],
                    timestamp=datetime.fromisoformat(match_dict["timestamp"]),
                    status=match_dict["status"]
                )
                
                # Store in database
                await self.agent.db.add_match(match)
                
                # Update statuses
                await self.agent.db.update_request_status(match.request_id, "matched")
                await self.agent.db.update_available_materials_status(match.available_materials_id, "matched")
                
                # Notify the matcher that match was processed
                response_msg = Message(
                    to=msg.sender,
                    body=f"Match {match.id} processed and stored",
                    subject="MatchProcessed"
                )
                await self.send(response_msg)
                
    class ProduceAvailableMaterialsBehaviour(CyclicBehaviour):
        async def run(self):
            # Periodically check for available materials and propagate them
            # In a real system, this would be triggered by actual material availability
            
            # For demonstration, we'll just send a sample material
            materials = AvailableMaterials(
                id=str(uuid.uuid4()),
                provider_id=str(self.agent.jid),
                resource_type="food_supplies",
                quantity=20,
                location="Distribution Center X"
            )
            
            self.agent.logger.info(f"Producing available materials: {materials.id}")
            
            # Send materials to Matcher
            msg = Message(
                to="matcher@localhost",
                body=str(materials.__dict__),
                subject="AvailableMaterials"
            )
            await self.send(msg)
            
            # Wait for a while before producing next materials
            await asyncio.sleep(20)