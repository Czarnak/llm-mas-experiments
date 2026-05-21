import asyncio
import uuid
from typing import Dict, List, Optional
from datetime import datetime
from .agent import Agent, Message
from .models import *
from .message_broker import MessageBroker


class RegionalCoordinatorAgent(Agent):
    def __init__(self, agent_id: str, broker: MessageBroker):
        super().__init__(agent_id, "RegionalCoordinator")
        self.broker = broker
        self.parking_agents: Dict[str, str] = {}  # parking_id -> agent_id
        self.user_agents: Dict[str, str] = {}  # user_id -> agent_id
        self.reservations: Dict[str, Reservation] = {}  # reservation_id -> Reservation

    async def handle_message(self, message: Message):
        if message.protocol == "SendOfferRequestToLocalAgents":
            await self._handle_offer_request(message)
        elif message.protocol == "SendReservationRequestToLocalAgent":
            await self._handle_reservation_request(message)
        elif message.protocol == "SendReservationModificationRequestToLocalAgent":
            await self._handle_reservation_modification_request(message)
        elif message.protocol == "SendOfferToUser":
            await self._handle_send_offer_to_user(message)
        elif message.protocol == "SendInformationToUser":
            await self._handle_send_information_to_user(message)
        elif message.protocol == "AwaitAgentOfferResponse":
            await self._handle_agent_offer_response(message)
        elif message.protocol == "AwaitAgentReservationResponse":
            await self._handle_agent_reservation_response(message)

    async def _handle_offer_request(self, message: Message):
        # Send request to all local parking agents
        localization = Localization(**message.content["localization"])
        timeslot = ReservationTimeslot(**message.content["reservation_timeslot"])
        
        # Create a request for each parking agent
        for parking_id, agent_id in self.parking_agents.items():
            parking_message = Message(
                sender=self.agent_id,
                receiver=agent_id,
                protocol="AwaitOfferRequest",
                content={
                    "localization": localization.dict(),
                    "reservation_timeslot": timeslot.dict()
                },
                message_id=str(uuid.uuid4())
            )
            await self.broker._handle_message(parking_message)

    async def _handle_reservation_request(self, message: Message):
        # Send reservation request to the specific parking agent
        parking_id = message.content["parking_id"]
        if parking_id in self.parking_agents:
            parking_agent_id = self.parking_agents[parking_id]
            reservation_message = Message(
                sender=self.agent_id,
                receiver=parking_agent_id,
                protocol="AwaitReservationRequest",
                content=message.content,
                message_id=str(uuid.uuid4())
            )
            await self.broker._handle_message(reservation_message)

    async def _handle_reservation_modification_request(self, message: Message):
        # Send modification request to the specific parking agent
        parking_id = message.content["parking_id"]
        if parking_id in self.parking_agents:
            parking_agent_id = self.parking_agents[parking_id]
            modification_message = Message(
                sender=self.agent_id,
                receiver=parking_agent_id,
                protocol="AwaitReservationModificationRequest",
                content=message.content,
                message_id=str(uuid.uuid4())
            )
            await self.broker._handle_message(modification_message)

    async def _handle_send_offer_to_user(self, message: Message):
        # Send consolidated offers to user
        user_agent_id = self.user_agents.get(message.content.get("user_id"))
        if user_agent_id:
            offer_message = Message(
                sender=self.agent_id,
                receiver=user_agent_id,
                protocol="SendOfferToUser",
                content=message.content,
                message_id=str(uuid.uuid4())
            )
            await self.broker._handle_message(offer_message)

    async def _handle_send_information_to_user(self, message: Message):
        # Send reservation information to user
        user_agent_id = self.user_agents.get(message.content.get("user_id"))
        if user_agent_id:
            info_message = Message(
                sender=self.agent_id,
                receiver=user_agent_id,
                protocol="SendInformationToUser",
                content=message.content,
                message_id=str(uuid.uuid4())
            )
            await self.broker._handle_message(info_message)

    async def _handle_agent_offer_response(self, message: Message):
        # Collect responses from parking agents and consolidate offers
        user_id = message.content.get("user_id")
        
        # Remove this parking agent from pending requests
        if user_id in self.pending_offer_requests:
            if message.sender in self.pending_offer_requests[user_id]:
                self.pending_offer_requests[user_id].remove(message.sender)
                
        # If we've received all responses, consolidate and send to user
        if user_id in self.pending_offer_requests and not self.pending_offer_requests[user_id]:
            # In a real system, we would consolidate the offers
            # For demo purposes, we'll create some sample offers
            offers = [
                ConsolidatedOffer(
                    parking_id="parking_1",
                    name="Parking Lot A",
                    location=Localization(latitude=52.2297, longitude=21.0122, radius_km=2.0),
                    available_spots=25,
                    price_per_hour=5.0,
                ),
                ConsolidatedOffer(
                    parking_id="parking_2",
                    name="Parking Lot B",
                    location=Localization(latitude=52.2300, longitude=21.0150, radius_km=2.0),
                    available_spots=15,
                    price_per_hour=7.0,
                )
            ]
            
            # Send consolidated offers to user
            offer_message = Message(
                sender=self.agent_id,
                receiver=self.user_agents[user_id],
                protocol="SendOfferToUser",
                content={
                    "user_id": user_id,
                    "offers": [offer.dict() for offer in offers]
                },
                message_id=str(uuid.uuid4())
            )
            await self.broker._handle_message(offer_message)

    async def _handle_agent_reservation_response(self, message: Message):
        # Handle reservation response from parking agent
        # Update reservation status and send to user
        user_id = message.content.get("user_id")
        
        # Send response to user
        if user_id in self.user_agents:
            info_message = Message(
                sender=self.agent_id,
                receiver=self.user_agents[user_id],
                protocol="SendInformationToUser",
                content=message.content,
                message_id=str(uuid.uuid4())
            )
            await self.broker._handle_message(info_message)

    def add_parking_agent(self, parking_id: str, agent_id: str):
        self.parking_agents[parking_id] = agent_id

    def add_user_agent(self, user_id: str, agent_id: str):
        self.user_agents[user_id] = agent_id

    def get_role(self) -> str:
        return "RegionalCoordinator"
