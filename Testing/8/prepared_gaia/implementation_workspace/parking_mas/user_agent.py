import asyncio
import uuid
from typing import Dict, List, Optional
from datetime import datetime
from .agent import Agent, Message
from .models import *
from .message_broker import MessageBroker


class UserAgent(Agent):
    def __init__(self, agent_id: str, broker: MessageBroker, user_data: User):
        super().__init__(agent_id, "User")
        self.broker = broker
        self.user_data = user_data
        self.active_reservations: Dict[str, Reservation] = {}
        self.consolidated_offers: List[ConsolidatedOffer] = []

    async def handle_message(self, message: Message):
        if message.protocol == "SendMyParkingRequest":
            await self._handle_send_parking_request(message)
        elif message.protocol == "AwaitOfferResponse":
            await self._handle_await_offer_response(message)
        elif message.protocol == "SendMyReservationRequest":
            await self._handle_send_reservation_request(message)
        elif message.protocol == "AwaitReservationResponse":
            await self._handle_await_reservation_response(message)
        elif message.protocol == "SendOfferToUser":
            await self._handle_send_offer_to_user(message)
        elif message.protocol == "SendInformationToUser":
            await self._handle_send_information_to_user(message)

    async def _handle_send_parking_request(self, message: Message):
        # Send request to coordinator for parking offers
        coordinator_id = message.content.get("coordinator_id")
        localization = Localization(**message.content["localization"])
        timeslot = ReservationTimeslot(**message.content["reservation_timeslot"])
        
        # Create request to coordinator
        request_message = Message(
            sender=self.agent_id,
            receiver=coordinator_id,
            protocol="SendOfferRequestToLocalAgents",
            content={
                "user_id": self.user_data.user_id,
                "localization": localization.dict(),
                "reservation_timeslot": timeslot.dict()
            },
            message_id=str(uuid.uuid4())
        )
        await self.broker._handle_message(request_message)

    async def _handle_await_offer_response(self, message: Message):
        # Process offers received from coordinator
        offers = message.content.get("offers", [])
        self.consolidated_offers = [ConsolidatedOffer(**offer) for offer in offers]
        
        # For demo purposes, just print the offers
        print(f"User {self.user_data.name} received offers:")
        for offer in self.consolidated_offers:
            print(f"  - {offer.name}: {offer.available_spots} spots available at ${offer.price_per_hour}/hr")

    async def _handle_send_reservation_request(self, message: Message):
        # Send reservation request to coordinator
        coordinator_id = message.content.get("coordinator_id")
        
        reservation_message = Message(
            sender=self.agent_id,
            receiver=coordinator_id,
            protocol="SendReservationRequestToLocalAgent",
            content=message.content,
            message_id=str(uuid.uuid4())
        )
        await self.broker._handle_message(reservation_message)

    async def _handle_await_reservation_response(self, message: Message):
        # Process reservation response from coordinator
        status = message.content.get("status")
        if status == "confirmed":
            reservation_id = message.content.get("reservation_id")
            reservation = Reservation(
                reservation_id=reservation_id,
                user_id=self.user_data.user_id,
                parking_id=message.content.get("parking_id"),
                timeslot=ReservationTimeslot(**message.content.get("timeslot", {}))
            )
            self.active_reservations[reservation_id] = reservation
            print(f"Reservation confirmed for user {self.user_data.name}: {reservation_id}")
        else:
            print(f"Reservation failed for user {self.user_data.name}: {message.content.get('reason', 'Unknown error')}")

    async def _handle_send_offer_to_user(self, message: Message):
        # Handle offers sent from coordinator
        await self._handle_await_offer_response(message)

    async def _handle_send_information_to_user(self, message: Message):
        # Handle information sent from coordinator
        await self._handle_await_reservation_response(message)

    def get_role(self) -> str:
        return "User"
