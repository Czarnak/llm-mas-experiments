import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
from typing import List
from datetime import datetime

from models.user import User
from models.parking_lot import ParkingLot
from utils.logger import setup_logger


class UserAgent(Agent):
    def __init__(self, jid: str, password: str, user: User):
        super().__init__(jid, password)
        self.user = user
        self.logger = setup_logger(f"UserAgent-{user.id}")
        
    async def setup(self):
        self.logger.info(f"User agent {self.user.name} with JID {self.jid} is ready")
        
        # Add behaviours
        check_availability_behaviour = CheckAvailabilityBehaviour()
        self.add_behaviour(check_availability_behaviour)
        
        initiate_reservation_behaviour = InitiateReservationBehaviour()
        self.add_behaviour(initiate_reservation_behaviour)
        
        cancel_reservation_behaviour = CancelReservationBehaviour()
        self.add_behaviour(cancel_reservation_behaviour)
        
        extend_reservation_behaviour = ExtendReservationBehaviour()
        self.add_behaviour(extend_reservation_behaviour)
        
        modify_reservation_behaviour = ModifyReservationBehaviour()
        self.add_behaviour(modify_reservation_behaviour)


class CheckAvailabilityBehaviour(CyclicBehaviour):
    async def run(self):
        self.logger = setup_logger("CheckAvailabilityBehaviour")
        
        # Create a message to request parking availability
        msg = Message(to="reservation_system@localhost", 
                      sender=str(self.agent.jid),
                      subject="CheckParkingAvailability",
                      body="Check availability for user at location: {}".format(self.agent.user.location))
        
        # Send the message
        await self.send(msg)
        self.logger.info("Sent availability check request")
        
        # Wait for response
        msg = await self.receive(timeout=10)
        if msg:
            self.logger.info(f"Received availability response: {msg.body}")
            # Process the response here
        else:
            self.logger.warning("No response received for availability check")
        
        # Wait before next check
        await asyncio.sleep(5)


class InitiateReservationBehaviour(CyclicBehaviour):
    async def run(self):
        self.logger = setup_logger("InitiateReservationBehaviour")
        
        # For demonstration, we'll simulate reservation initiation
        # In a real system, this would be triggered by user interaction
        
        # Wait for a while before trying to make a reservation
        await asyncio.sleep(10)
        
        # Simulate making a reservation
        msg = Message(to="reservation_system@localhost", 
                      sender=str(self.agent.jid),
                      subject="InitiateReservation",
                      body="Initiate reservation for user {} at parking lot {}".format(
                          self.agent.user.id, "lot_001"))
        
        # Send the message
        await self.send(msg)
        self.logger.info("Sent reservation initiation request")
        
        # Wait for response
        msg = await self.receive(timeout=10)
        if msg:
            self.logger.info(f"Received reservation response: {msg.body}")
        else:
            self.logger.warning("No response received for reservation")


class CancelReservationBehaviour(CyclicBehaviour):
    async def run(self):
        self.logger = setup_logger("CancelReservationBehaviour")
        
        # This would be triggered by user action
        await asyncio.sleep(30)
        
        # Simulate canceling a reservation
        msg = Message(to="reservation_system@localhost", 
                      sender=str(self.agent.jid),
                      subject="CancelReservation",
                      body="Cancel reservation {}".format("res_001"))
        
        # Send the message
        await self.send(msg)
        self.logger.info("Sent reservation cancellation request")
        
        # Wait for response
        msg = await self.receive(timeout=10)
        if msg:
            self.logger.info(f"Received cancellation response: {msg.body}")
        else:
            self.logger.warning("No response received for cancellation")


class ExtendReservationBehaviour(CyclicBehaviour):
    async def run(self):
        self.logger = setup_logger("ExtendReservationBehaviour")
        
        # This would be triggered by user action
        await asyncio.sleep(40)
        
        # Simulate extending a reservation
        msg = Message(to="reservation_system@localhost", 
                      sender=str(self.agent.jid),
                      subject="ExtendReservation",
                      body="Extend reservation {} to new end time".format("res_001"))
        
        # Send the message
        await self.send(msg)
        self.logger.info("Sent reservation extension request")
        
        # Wait for response
        msg = await self.receive(timeout=10)
        if msg:
            self.logger.info(f"Received extension response: {msg.body}")
        else:
            self.logger.warning("No response received for extension")


class ModifyReservationBehaviour(CyclicBehaviour):
    async def run(self):
        self.logger = setup_logger("ModifyReservationBehaviour")
        
        # This would be triggered by user action
        await asyncio.sleep(50)
        
        # Simulate modifying a reservation
        msg = Message(to="reservation_system@localhost", 
                      sender=str(self.agent.jid),
                      subject="ModifyReservationTime",
                      body="Modify reservation {} to new time slot".format("res_001"))
        
        # Send the message
        await self.send(msg)
        self.logger.info("Sent reservation modification request")
        
        # Wait for response
        msg = await self.receive(timeout=10)
        if msg:
            self.logger.info(f"Received modification response: {msg.body}")
        else:
            self.logger.warning("No response received for modification")