import asyncio
import uuid
from typing import Dict, List
from .agent import Agent, Message
from .message_broker import MessageBroker
from .regional_coordinator import RegionalCoordinatorAgent
from .parking_agent import ParkingAgent
from .user_agent import UserAgent
from .models import *


class ParkingMAS:
    def __init__(self):
        self.broker = MessageBroker()
        self.agents: Dict[str, Agent] = {}
        self.coordinators: Dict[str, RegionalCoordinatorAgent] = {}
        self.parking_agents: Dict[str, ParkingAgent] = {}
        self.user_agents: Dict[str, UserAgent] = {}

    async def start(self):
        print("Starting Parking Multi-Agent System...")
        await self.broker.start()
        
        # Create a regional coordinator
        coordinator = RegionalCoordinatorAgent("coordinator_1", self.broker)
        await coordinator.start()
        self.coordinators["coordinator_1"] = coordinator
        self.agents["coordinator_1"] = coordinator
        
        # Create parking agents
        parking_data1 = ParkingAgentState(
            parking_id="parking_1",
            name="Parking Lot A",
            location=Localization(latitude=52.2297, longitude=21.0122, radius_km=2.0),
            total_spots=50,
            price_per_hour=5.0,
            min_price=10.0,
            reservations=[]
        )
        
        parking_data2 = ParkingAgentState(
            parking_id="parking_2",
            name="Parking Lot B",
            location=Localization(latitude=52.2300, longitude=21.0150, radius_km=2.0),
            total_spots=30,
            price_per_hour=7.0,
            min_price=15.0,
            reservations=[]
        )
        
        parking_agent1 = ParkingAgent("parking_1_agent", self.broker, parking_data1)
        parking_agent2 = ParkingAgent("parking_2_agent", self.broker, parking_data2)
        
        await parking_agent1.start()
        await parking_agent2.start()
        
        self.parking_agents["parking_1"] = parking_agent1
        self.parking_agents["parking_2"] = parking_agent2
        self.agents["parking_1_agent"] = parking_agent1
        self.agents["parking_2_agent"] = parking_agent2
        
        # Connect parking agents to coordinator
        coordinator.add_parking_agent("parking_1", "parking_1_agent")
        coordinator.add_parking_agent("parking_2", "parking_2_agent")
        
        # Create user agents
        user1 = User(user_id="user_1", name="John Doe")
        user2 = User(user_id="user_2", name="Jane Smith")
        
        user_agent1 = UserAgent("user_1_agent", self.broker, user1)
        user_agent2 = UserAgent("user_2_agent", self.broker, user2)
        
        await user_agent1.start()
        await user_agent2.start()
        
        self.user_agents["user_1"] = user_agent1
        self.user_agents["user_2"] = user_agent2
        self.agents["user_1_agent"] = user_agent1
        self.agents["user_2_agent"] = user_agent2
        
        # Connect user agents to coordinator
        coordinator.add_user_agent("user_1", "user_1_agent")
        coordinator.add_user_agent("user_2", "user_2_agent")
        
        print("Parking Multi-Agent System started successfully!")

    async def stop(self):
        print("Stopping Parking Multi-Agent System...")
        for agent in self.agents.values():
            await agent.stop()
        await self.broker.stop()
        print("Parking Multi-Agent System stopped.")

    async def simulate_user_request(self):
        print("\n=== Simulating User Request ===")
        
        # Create a request for parking near a hotel
        user_agent = self.user_agents["user_1"]
        
        localization = Localization(latitude=52.2300, longitude=21.0150, radius_km=2.0)
        timeslot = ReservationTimeslot(
            start_time=datetime.now(),
            end_time=datetime.now().replace(hour=datetime.now().hour + 2)
        )
        
        # Send request to coordinator
        request_message = Message(
            sender="user_1_agent",
            receiver="coordinator_1",
            protocol="SendMyParkingRequest",
            content={
                "coordinator_id": "coordinator_1",
                "localization": localization.dict(),
                "reservation_timeslot": timeslot.dict()
            },
            message_id=str(uuid.uuid4())
        )
        
        await self.broker._handle_message(request_message)
        
        # Wait a bit for responses
        await asyncio.sleep(1)
        
        # Simulate reservation request
        print("\n=== Simulating Reservation Request ===")
        reservation_message = Message(
            sender="user_1_agent",
            receiver="coordinator_1",
            protocol="SendMyReservationRequest",
            content={
                "coordinator_id": "coordinator_1",
                "user_id": "user_1",
                "parking_id": "parking_1",
                "reservation_timeslot": timeslot.dict()
            },
            message_id=str(uuid.uuid4())
        )
        
        await self.broker._handle_message(reservation_message)
        
        # Wait for processing
        await asyncio.sleep(1)

    async def run_demo(self):
        await self.start()
        await self.simulate_user_request()
        await asyncio.sleep(2)
        await self.stop()
