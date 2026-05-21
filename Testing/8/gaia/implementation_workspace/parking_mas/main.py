import asyncio
import sys
from datetime import datetime

from agents.user_agent import UserAgent
from agents.reservation_system_agent import ReservationSystemAgent
from agents.parking_lot_agent import ParkingLotAgent
from agents.payment_processor_agent import PaymentProcessorAgent
from models.user import User
from models.parking_lot import ParkingLot


def run_simulation():
    print("Starting Parking Management Multi-Agent System simulation...")
    
    # Create agents
    # User Agent
    user = User(id="user_001", name="John Doe", email="john@example.com", location="Near Hotel Mariot")
    user_agent = UserAgent("user_001@localhost", "user_password", user)
    
    # Reservation System Agent
    reservation_system_agent = ReservationSystemAgent("reservation_system@localhost", "system_password")
    
    # Parking Lot Agents (multiple instances)
    parking_lot1 = ParkingLot(
        id="lot_001",
        name="Parking Lot A",
        location="Near Hotel Mariot",
        total_spaces=50,
        available_spaces=30,
        price_per_hour=5.0
    )
    
    parking_lot2 = ParkingLot(
        id="lot_002",
        name="Parking Lot B",
        location="City Center",
        total_spaces=30,
        available_spaces=15,
        price_per_hour=7.0
    )
    
    parking_lot_agent1 = ParkingLotAgent("parking_lot_001@localhost", "lot_password", parking_lot1)
    parking_lot_agent2 = ParkingLotAgent("parking_lot_002@localhost", "lot_password", parking_lot2)
    
    # Payment Processor Agent
    payment_processor_agent = PaymentProcessorAgent("payment_processor@localhost", "payment_password")
    
    # Start all agents
    async def start_agents():
        await user_agent.start()
        await reservation_system_agent.start()
        await parking_lot_agent1.start()
        await parking_lot_agent2.start()
        await payment_processor_agent.start()
        
        print("All agents started successfully!")
        
        # Let the agents run for a while to demonstrate functionality
        await asyncio.sleep(60)
        
        # Stop agents
        await user_agent.stop()
        await reservation_system_agent.stop()
        await parking_lot_agent1.stop()
        await parking_lot_agent2.stop()
        await payment_processor_agent.stop()
        
        print("Simulation completed.")
        
    # Run the simulation
    asyncio.run(start_agents())


if __name__ == "__main__":
    run_simulation()