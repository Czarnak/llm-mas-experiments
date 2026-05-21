import os
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# Import our models and services (using absolute imports)
from parking_system.models.parking_lot import ParkingLot
from parking_system.models.reservation import Reservation, ReservationRequest
from parking_system.models.user import User
from parking_system.services.database import init_db, get_db
from parking_system.services.parking_lot_service import ParkingLotService
from parking_system.services.reservation_service import ReservationService
from parking_system.services.search_service import SearchService

# Import our agents
from parking_system.agents.user_agent import UserAgent
from parking_system.agents.parking_search_agent import ParkingSearchAgent
from parking_system.agents.availability_agent import AvailabilityAgent
from parking_system.agents.reservation_agent import ReservationAgent
from parking_system.agents.payment_agent import PaymentAgent
from parking_system.agents.notification_agent import NotificationAgent

# Initialize FastAPI app
app = FastAPI(title="FindMyParking API", version="1.0.0")

# Initialize database
init_db()

# Create service instances
# Note: In a real application, these would be injected properly
search_service = SearchService()

# Initialize agents
user_agent = UserAgent(search_service)
search_agent = ParkingSearchAgent(search_service)
availability_agent = AvailabilityAgent(ParkingLotService(next(get_db())))
reservation_agent = ReservationAgent(ReservationService(next(get_db()), availability_agent))
payment_agent = PaymentAgent()
notification_agent = NotificationAgent()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/parking-lots", response_model=List[ParkingLot])
async def get_parking_lots():
    try:
        parking_lot_service = ParkingLotService(next(get_db()))
        lots = parking_lot_service.get_parking_lots()
        return lots
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/parking-lots/available", response_model=List[ParkingLot])
async def get_available_parking_lots():
    try:
        parking_lot_service = ParkingLotService(next(get_db()))
        lots = parking_lot_service.get_available_parking_lots()
        return lots
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/parking-lots/nearby", response_model=List[ParkingLot])
async def find_nearby_parking(lat: float, lng: float):
    try:
        lots = search_agent.find_nearby_parking({"lat": lat, "lng": lng})
        return lots
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reservations", response_model=Reservation)
async def create_reservation(reservation_request: ReservationRequest):
    try:
        # Create the reservation
        reservation = reservation_agent.create_reservation(reservation_request)
        if not reservation:
            raise HTTPException(status_code=400, detail="Failed to create reservation")
        
        # Process payment
        payment_success = payment_agent.process_payment(reservation)
        if not payment_success:
            raise HTTPException(status_code=400, detail="Payment processing failed")
        
        # Send confirmation
        notification_agent.send_confirmation(reservation)
        
        return reservation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reservations/{reservation_id}/cancel")
async def cancel_reservation(reservation_id: str):
    try:
        success = reservation_agent.cancel_reservation(reservation_id)
        if not success:
            raise HTTPException(status_code=404, detail="Reservation not found")
        
        # Get the reservation to send notification
        reservation = reservation_agent.get_reservation(reservation_id)
        if reservation:
            notification_agent.send_cancellation_notification(reservation)
        
        return {"message": "Reservation cancelled successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Demo function to simulate the user story
async def demo_user_story():
    print("=== FindMyParking Demo ===")
    print("User story: Find parking near Mariot hotel")
    
    # Simulate hotel location (Mariot hotel in Warsaw)
    hotel_location = {"lat": 52.2297, "lng": 21.0122}
    
    # Find nearby parking lots
    print("\n1. Searching for parking lots near the hotel...")
    parking_lots = search_agent.find_parking_for_hotel("Mariot Hotel", hotel_location)
    
    # Display results
    notification_agent.send_availability_notification(parking_lots)
    
    # Check availability and make reservation
    if parking_lots:
        print("\n2. Making reservation for the cheapest available parking...")
        first_lot = parking_lots[0]
        
        # Create a reservation request
        reservation_request = ReservationRequest(
            user_id="user_123",
            parking_lot_id=first_lot.id,
            start_time=datetime.utcnow() + timedelta(hours=1),  # Start in 1 hour
            end_time=datetime.utcnow() + timedelta(hours=4)     # End in 4 hours
        )
        
        # Create reservation
        reservation = reservation_agent.create_reservation(reservation_request)
        if reservation:
            # Process payment
            payment_agent.process_payment(reservation)
            
            # Send confirmation
            notification_agent.send_confirmation(reservation)
            
            print(f"\n3. Reservation successful!")
            print(f"   Reservation ID: {reservation.id}")
            print(f"   Cost: {reservation.cost} PLN")
            print(f"   Duration: {reservation.start_time} to {reservation.end_time}")
        else:
            print("\n3. Failed to make reservation - no available spots")
    else:
        print("\n1. No parking lots found in the area")
    
    print("\n=== Demo Complete ===")

if __name__ == "__main__":
    import asyncio
    asyncio.run(demo_user_story())