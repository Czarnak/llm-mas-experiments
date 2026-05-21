import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message
from spade.template import Template
from typing import List, Dict, Optional
from datetime import datetime

from models.parking_lot import ParkingLot
from models.reservation import Reservation
from models.user import User
from models.payment import PaymentDetails
from utils.logger import setup_logger


class ReservationSystemAgent(Agent):
    def __init__(self, jid: str, password: str):
        super().__init__(jid, password)
        self.logger = setup_logger("ReservationSystemAgent")
        self.parking_lots: Dict[str, ParkingLot] = {}
        self.reservations: Dict[str, Reservation] = {}
        self.users: Dict[str, User] = {}
        
    async def setup(self):
        self.logger.info("Reservation System agent is ready")
        
        # Add behaviours
        check_availability_behaviour = CheckAvailabilityBehaviour()
        self.add_behaviour(check_availability_behaviour)
        
        initiate_reservation_behaviour = InitiateReservationBehaviour()
        self.add_behaviour(initiate_reservation_behaviour)
        
        confirm_reservation_behaviour = ConfirmReservationBehaviour()
        self.add_behaviour(confirm_reservation_behaviour)
        
        cancel_reservation_behaviour = CancelReservationBehaviour()
        self.add_behaviour(cancel_reservation_behaviour)
        
        extend_reservation_behaviour = ExtendReservationBehaviour()
        self.add_behaviour(extend_reservation_behaviour)
        
        modify_reservation_behaviour = ModifyReservationBehaviour()
        self.add_behaviour(modify_reservation_behaviour)
        
        process_payment_behaviour = ProcessPaymentBehaviour()
        self.add_behaviour(process_payment_behaviour)
        
        # Initialize with some sample data
        self._initialize_sample_data()
        
    def _initialize_sample_data(self):
        # Create sample parking lots
        lot1 = ParkingLot(
            id="lot_001",
            name="Parking Lot A",
            location="Near Hotel Mariot",
            total_spaces=50,
            available_spaces=30,
            price_per_hour=5.0
        )
        
        lot2 = ParkingLot(
            id="lot_002",
            name="Parking Lot B",
            location="City Center",
            total_spaces=30,
            available_spaces=15,
            price_per_hour=7.0
        )
        
        lot3 = ParkingLot(
            id="lot_003",
            name="Parking Lot C",
            location="University Area",
            total_spaces=20,
            available_spaces=8,
            price_per_hour=4.0
        )
        
        self.parking_lots[lot1.id] = lot1
        self.parking_lots[lot2.id] = lot2
        self.parking_lots[lot3.id] = lot3
        
        # Create sample users
        user1 = User(
            id="user_001",
            name="John Doe",
            email="john@example.com",
            location="Near Hotel Mariot"
        )
        
        self.users[user1.id] = user1


class CheckAvailabilityBehaviour(CyclicBehaviour):
    async def run(self):
        self.logger = setup_logger("CheckAvailabilityBehaviour")
        
        # Wait for incoming message
        msg = await self.receive(timeout=10)
        if msg and msg.get_metadata("subject") == "CheckParkingAvailability":
            self.logger.info(f"Received availability check request from {msg.sender}")
            
            # Extract user location from message
            location = msg.body.split(": ")[1] if ": " in msg.body else "Unknown"
            
            # Find available lots near the location
            available_lots = []
            for lot in self.agent.parking_lots.values():
                if lot.is_space_available() and location in lot.location:
                    available_lots.append(lot)
            
            # Sort by price
            available_lots.sort(key=lambda x: x.price_per_hour)
            
            # Create response
            response_body = "Available lots:\n"
            for lot in available_lots:
                response_body += f"- {lot.name}: {lot.available_spaces} spaces available, ${lot.price_per_hour}/hour\n"
            
            if not available_lots:
                response_body = "No available parking lots found in the requested area."
            
            # Send response
            response = Message(to=str(msg.sender),
                              sender=str(self.agent.jid),
                              subject="AvailableParkingLots",
                              body=response_body)
            await self.send(response)
            self.logger.info("Sent availability response")


class InitiateReservationBehaviour(CyclicBehaviour):
    async def run(self):
        self.logger = setup_logger("InitiateReservationBehaviour")
        
        # Wait for incoming message
        msg = await self.receive(timeout=10)
        if msg and msg.get_metadata("subject") == "InitiateReservation":
            self.logger.info(f"Received reservation initiation request from {msg.sender}")
            
            # Extract reservation details
            try:
                # For simplicity, parsing the message body
                parts = msg.body.split(" ")
                user_id = parts[4]  # user ID from message
                lot_id = parts[7]  # lot ID from message
                
                # Check if lot exists
                if lot_id not in self.agent.parking_lots:
                    response = Message(to=str(msg.sender),
                                      sender=str(self.agent.jid),
                                      subject="ReservationStatus",
                                      body="Error: Parking lot not found")
                    await self.send(response)
                    return
                
                lot = self.agent.parking_lots[lot_id]
                
                # Check if space is available
                if not lot.is_space_available():
                    response = Message(to=str(msg.sender),
                                      sender=str(self.agent.jid),
                                      subject="ReservationStatus",
                                      body="Error: No available spaces")
                    await self.send(response)
                    return
                
                # Create reservation (simplified)
                reservation_id = f"res_{len(self.agent.reservations) + 1:03d}"
                start_time = datetime.now()
                end_time = start_time.replace(hour=start_time.hour + 2)  # 2 hours reservation
                
                cost = lot.get_cost(start_time, end_time)
                
                reservation = Reservation(
                    id=reservation_id,
                    user_id=user_id,
                    parking_lot_id=lot_id,
                    start_time=start_time,
                    end_time=end_time,
                    cost=cost
                )
                
                # Store reservation
                self.agent.reservations[reservation_id] = reservation
                
                # Reserve space in parking lot
                lot.reserve_space(reservation_id)
                
                # Send confirmation to user
                response = Message(to=str(msg.sender),
                                  sender=str(self.agent.jid),
                                  subject="ReservationConfirmation",
                                  body=f"Reservation confirmed. ID: {reservation_id}, Cost: ${cost}")
                await self.send(response)
                
                # Send request to parking lot to confirm reservation
                confirm_msg = Message(to=f"parking_lot_{lot_id}@localhost",
                                     sender=str(self.agent.jid),
                                     subject="ConfirmReservation",
                                     body=f"Confirm reservation {reservation_id} for lot {lot_id}")
                await self.send(confirm_msg)
                
                self.logger.info(f"Reservation {reservation_id} created and confirmed")
                
            except Exception as e:
                self.logger.error(f"Error processing reservation: {e}")
                response = Message(to=str(msg.sender),
                                  sender=str(self.agent.jid),
                                  subject="ReservationStatus",
                                  body="Error processing reservation")
                await self.send(response)


class ConfirmReservationBehaviour(CyclicBehaviour):
    async def run(self):
        self.logger = setup_logger("ConfirmReservationBehaviour")
        
        # Wait for incoming message
        msg = await self.receive(timeout=10)
        if msg and msg.get_metadata("subject") == "ConfirmReservation":
            self.logger.info(f"Received reservation confirmation request from {msg.sender}")
            
            # For now, just acknowledge the confirmation
            response = Message(to=str(msg.sender),
                              sender=str(self.agent.jid),
                              subject="SpaceBlocked",
                              body="Space successfully blocked")
            await self.send(response)
            self.logger.info("Sent space blocked confirmation")


class CancelReservationBehaviour(CyclicBehaviour):
    async def run(self):
        self.logger = setup_logger("CancelReservationBehaviour")
        
        # Wait for incoming message
        msg = await self.receive(timeout=10)
        if msg and msg.get_metadata("subject") == "CancelReservation":
            self.logger.info(f"Received cancellation request from {msg.sender}")
            
            # Extract reservation ID
            try:
                reservation_id = msg.body.split(" ")[2]  # reservation ID from message
                
                if reservation_id in self.agent.reservations:
                    reservation = self.agent.reservations[reservation_id]
                    
                    # Release space in parking lot
                    lot = self.agent.parking_lots.get(reservation.parking_lot_id)
                    if lot:
                        lot.release_space(reservation_id)
                        
                    # Update reservation status
                    reservation.status = "cancelled"
                    
                    # Send confirmation
                    response = Message(to=str(msg.sender),
                                      sender=str(self.agent.jid),
                                      subject="CancellationConfirmation",
                                      body=f"Reservation {reservation_id} cancelled successfully")
                    await self.send(response)
                    
                    self.logger.info(f"Reservation {reservation_id} cancelled")
                else:
                    response = Message(to=str(msg.sender),
                                      sender=str(self.agent.jid),
                                      subject="CancellationConfirmation",
                                      body="Error: Reservation not found")
                    await self.send(response)
                    
            except Exception as e:
                self.logger.error(f"Error processing cancellation: {e}")
                response = Message(to=str(msg.sender),
                                  sender=str(self.agent.jid),
                                  subject="CancellationConfirmation",
                                  body="Error processing cancellation")
                await self.send(response)


class ExtendReservationBehaviour(CyclicBehaviour):
    async def run(self):
        self.logger = setup_logger("ExtendReservationBehaviour")
        
        # Wait for incoming message
        msg = await self.receive(timeout=10)
        if msg and msg.get_metadata("subject") == "ExtendReservation":
            self.logger.info(f"Received extension request from {msg.sender}")
            
            # For now, just simulate the process
            response = Message(to=str(msg.sender),
                              sender=str(self.agent.jid),
                              subject="ExtensionConfirmation",
                              body="Reservation extended successfully")
            await self.send(response)
            self.logger.info("Sent extension confirmation")


class ModifyReservationBehaviour(CyclicBehaviour):
    async def run(self):
        self.logger = setup_logger("ModifyReservationBehaviour")
        
        # Wait for incoming message
        msg = await self.receive(timeout=10)
        if msg and msg.get_metadata("subject") == "ModifyReservationTime":
            self.logger.info(f"Received modification request from {msg.sender}")
            
            # For now, just simulate the process
            response = Message(to=str(msg.sender),
                              sender=str(self.agent.jid),
                              subject="ModificationConfirmation",
                              body="Reservation modified successfully")
            await self.send(response)
            self.logger.info("Sent modification confirmation")


class ProcessPaymentBehaviour(CyclicBehaviour):
    async def run(self):
        self.logger = setup_logger("ProcessPaymentBehaviour")
        
        # Wait for incoming message
        msg = await self.receive(timeout=10)
        if msg and msg.get_metadata("subject") == "ProcessPayment":
            self.logger.info(f"Received payment request from {msg.sender}")
            
            # For now, just simulate payment processing
            response = Message(to=str(msg.sender),
                              sender=str(self.agent.jid),
                              subject="PaymentConfirmation",
                              body="Payment processed successfully")
            await self.send(response)
            self.logger.info("Sent payment confirmation")