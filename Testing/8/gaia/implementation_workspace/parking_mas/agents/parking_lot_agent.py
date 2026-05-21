import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
from typing import Dict
from datetime import datetime

from models.parking_lot import ParkingLot
from utils.logger import setup_logger


class ParkingLotAgent(Agent):
    def __init__(self, jid: str, password: str, parking_lot: ParkingLot):
        super().__init__(jid, password)
        self.parking_lot = parking_lot
        self.logger = setup_logger(f"ParkingLotAgent-{parking_lot.id}")
        
    async def setup(self):
        self.logger.info(f"Parking lot agent {self.parking_lot.name} with JID {self.jid} is ready")
        
        # Add behaviours
        confirm_reservation_behaviour = ConfirmReservationBehaviour()
        self.add_behaviour(confirm_reservation_behaviour)


class ConfirmReservationBehaviour(CyclicBehaviour):
    async def run(self):
        self.logger = setup_logger("ConfirmReservationBehaviour")
        
        # Wait for incoming message
        msg = await self.receive(timeout=10)
        if msg and msg.get_metadata("subject") == "ConfirmReservation":
            self.logger.info(f"Received reservation confirmation request from {msg.sender}")
            
            # Extract reservation details
            try:
                # In a real implementation, we would verify the reservation details
                # For now, we'll just simulate the confirmation
                
                # Block the space (this is already done in the reservation system)
                # Just acknowledge that we've confirmed the reservation
                response = Message(to=str(msg.sender),
                                  sender=str(self.agent.jid),
                                  subject="SpaceBlocked",
                                  body="Space successfully blocked for reservation")
                await self.send(response)
                
                self.logger.info("Reservation confirmed and space blocked")
                
            except Exception as e:
                self.logger.error(f"Error confirming reservation: {e}")
                response = Message(to=str(msg.sender),
                                  sender=str(self.agent.jid),
                                  subject="SpaceBlocked",
                                  body="Error confirming reservation")
                await self.send(response)