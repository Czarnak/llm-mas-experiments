import asyncio
import uuid
from typing import Dict, List, Optional
from datetime import datetime
from .agent import Agent, Message
from .models import *
from .message_broker import MessageBroker


class ParkingAgent(Agent):
    def __init__(self, agent_id: str, broker: MessageBroker, parking_data: ParkingAgentState):
        super().__init__(agent_id, "Parking")
        self.broker = broker
        self.parking_data = parking_data
        self.reservations: Dict[str, Reservation] = {}

    async def handle_message(self, message: Message):
        if message.protocol == "AwaitOfferRequest":
            await self._handle_offer_request(message)
        elif message.protocol == "AwaitReservationRequest":
            await self._handle_reservation_request(message)
        elif message.protocol == "AwaitReservationModificationRequest":
            await self._handle_reservation_modification_request(message)
        elif message.protocol == "SendOfferResponse":
            await self._handle_send_offer_response(message)
        elif message.protocol == "SendInformationResponse":
            await self._handle_send_information_response(message)

    async def _handle_offer_request(self, message: Message):
        # Check parking spots availability
        localization = Localization(**message.content["localization"])
        timeslot = ReservationTimeslot(**message.content["reservation_timeslot"])
        user_id = message.content.get("user_id")
        
        # For simplicity, we'll check if there are any spots available
        available_spots = self.parking_data.total_spots - len(self.parking_data.reservations)
        
        response_content = {
            "parking_id": self.parking_data.parking_id,
            "name": self.parking_data.name,
            "location": localization.dict(),
            "available_spots": available_spots,
            "price_per_hour": self.parking_data.price_per_hour,
            "reservation_timeslot": timeslot.dict(),
            "user_id": user_id
        }
        
        # Send response back to coordinator
        response_message = Message(
            sender=self.agent_id,
            receiver=message.sender,
            protocol="SendOfferResponse",
            content=response_content,
            message_id=str(uuid.uuid4())
        )
        await self.broker._handle_message(response_message)

    async def _handle_reservation_request(self, message: Message):
        # Check if reservation can be made
        timeslot = ReservationTimeslot(**message.content["reservation_timeslot"])
        
        # Check if there are available spots
        available_spots = self.parking_data.total_spots - len(self.parking_data.reservations)
        
        if available_spots >= 1:
            # Create reservation
            reservation_id = str(uuid.uuid4())
            reservation = Reservation(
                reservation_id=reservation_id,
                user_id=message.content["user_id"],
                parking_id=self.parking_data.parking_id,
                timeslot=timeslot
            )
            
            # Add to reservations
            self.parking_data.reservations.append(reservation)
            self.reservations[reservation_id] = reservation
            
            response_content = {
                "reservation_id": reservation_id,
                "status": "confirmed",
                "parking_id": self.parking_data.parking_id,
                "timeslot": timeslot.dict()
            }
        else:
            response_content = {
                "status": "failed",
                "reason": "No available spots"
            }
            
        # Send response back to coordinator
        response_message = Message(
            sender=self.agent_id,
            receiver=message.sender,
            protocol="SendInformationResponse",
            content=response_content,
            message_id=str(uuid.uuid4())
        )
        await self.broker._handle_message(response_message)

    async def _handle_reservation_modification_request(self, message: Message):
        # Handle reservation modification (extend, change, cancel)
        reservation_id = message.content["reservation_id"]
        
        if reservation_id in self.reservations:
            reservation = self.reservations[reservation_id]
            
            # For simplicity, we'll handle cancellation and modification
            if "action" in message.content and message.content["action"] == "cancel":
                # Remove reservation
                self.parking_data.reservations = [r for r in self.parking_data.reservations if r.reservation_id != reservation_id]
                del self.reservations[reservation_id]
                
                response_content = {
                    "reservation_id": reservation_id,
                    "status": "cancelled"
                }
            elif "new_timeslot" in message.content:
                # Check if new timeslot is available
                new_timeslot = ReservationTimeslot(**message.content["new_timeslot"])
                
                # In a real system, we'd check for conflicts
                # For simplicity, we'll assume it's available
                reservation.timeslot = new_timeslot
                
                response_content = {
                    "reservation_id": reservation_id,
                    "status": "modified",
                    "timeslot": new_timeslot.dict()
                }
            else:
                response_content = {
                    "status": "failed",
                    "reason": "Invalid modification request"
                }
        else:
            response_content = {
                "status": "failed",
                "reason": "Reservation not found"
            }
            
        # Send response back to coordinator
        response_message = Message(
            sender=self.agent_id,
            receiver=message.sender,
            protocol="SendInformationResponse",
            content=response_content,
            message_id=str(uuid.uuid4())
        )
        await self.broker._handle_message(response_message)

    async def _handle_send_offer_response(self, message: Message):
        # This would be for sending responses back to coordinator
        pass

    async def _handle_send_information_response(self, message: Message):
        # This would be for sending responses back to coordinator
        pass

    def get_role(self) -> str:
        return "Parking"
