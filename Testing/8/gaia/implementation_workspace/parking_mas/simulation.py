import asyncio
from datetime import datetime, timedelta
from typing import Dict, List

# Models

class ParkingLot:
    def __init__(self, id: str, name: str, location: str, total_spaces: int, price_per_hour: float):
        self.id = id
        self.name = name
        self.location = location
        self.total_spaces = total_spaces
        self.available_spaces = total_spaces
        self.price_per_hour = price_per_hour
        self.reservations = []
        
    def reserve_space(self, reservation_id: str) -> bool:
        if self.available_spaces > 0:
            self.available_spaces -= 1
            self.reservations.append(reservation_id)
            return True
        return False
    
    def release_space(self, reservation_id: str) -> bool:
        if reservation_id in self.reservations:
            self.reservations.remove(reservation_id)
            self.available_spaces += 1
            return True
        return False
    
    def is_space_available(self) -> bool:
        return self.available_spaces > 0
    
    def get_cost(self, start_time: datetime, end_time: datetime) -> float:
        duration_hours = (end_time - start_time).total_seconds() / 3600
        return duration_hours * self.price_per_hour


class Reservation:
    def __init__(self, id: str, user_id: str, parking_lot_id: str, start_time: datetime, end_time: datetime):
        self.id = id
        self.user_id = user_id
        self.parking_lot_id = parking_lot_id
        self.start_time = start_time
        self.end_time = end_time
        self.status = "reserved"
        self.cost = 0.0
        self.payment_status = "pending"
        
    def extend_reservation(self, new_end_time: datetime) -> bool:
        if new_end_time > self.end_time:
            self.end_time = new_end_time
            return True
        return False
    
    def modify_reservation_time(self, new_start_time: datetime, new_end_time: datetime) -> bool:
        if new_start_time < new_end_time:
            self.start_time = new_start_time
            self.end_time = new_end_time
            return True
        return False


class User:
    def __init__(self, id: str, name: str, email: str, location: str):
        self.id = id
        self.name = name
        self.email = email
        self.location = location
        
    def update_location(self, new_location: str):
        self.location = new_location


class PaymentDetails:
    def __init__(self, id: str, reservation_id: str, amount: float, card_number: str, expiry_date: str, cvv: str):
        self.id = id
        self.reservation_id = reservation_id
        self.amount = amount
        self.card_number = card_number
        self.expiry_date = expiry_date
        self.cvv = cvv
        self.status = "pending"
        
    def validate_payment(self) -> bool:
        # Simple validation logic
        if (self.card_number and len(self.card_number) >= 13 and
            self.expiry_date and len(self.expiry_date) >= 5 and
            self.cvv and len(self.cvv) >= 3 and
            self.amount > 0):
            return True
        return False


class ReservationSystem:
    def __init__(self):
        self.parking_lots: Dict[str, ParkingLot] = {}
        self.reservations: Dict[str, Reservation] = {}
        self.users: Dict[str, User] = {}
        self._initialize_sample_data()
        
    def _initialize_sample_data(self):
        # Create sample parking lots
        lot1 = ParkingLot(
            id="lot_001",
            name="Parking Lot A",
            location="Near Hotel Mariot",
            total_spaces=50,
            price_per_hour=5.0
        )
        
        lot2 = ParkingLot(
            id="lot_002",
            name="Parking Lot B",
            location="City Center",
            total_spaces=30,
            price_per_hour=7.0
        )
        
        lot3 = ParkingLot(
            id="lot_003",
            name="Parking Lot C",
            location="University Area",
            total_spaces=20,
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
        
    def check_parking_availability(self, user_location: str, radius_km: float = 2.0) -> List[ParkingLot]:
        """Check available parking lots near the user location"""
        available_lots = []
        for lot in self.parking_lots.values():
            if lot.is_space_available() and user_location in lot.location:
                available_lots.append(lot)
        
        # Sort by price
        available_lots.sort(key=lambda x: x.price_per_hour)
        return available_lots
    
    def initiate_reservation(self, user_id: str, parking_lot_id: str, start_time: datetime, end_time: datetime) -> dict:
        """Initiate a parking reservation"""
        try:
            # Check if lot exists
            if parking_lot_id not in self.parking_lots:
                return {"success": False, "error": "Parking lot not found"}
            
            lot = self.parking_lots[parking_lot_id]
            
            # Check if space is available
            if not lot.is_space_available():
                return {"success": False, "error": "No available spaces"}
            
            # Create reservation
            reservation_id = f"res_{len(self.reservations) + 1:03d}"
            
            cost = lot.get_cost(start_time, end_time)
            
            reservation = Reservation(
                id=reservation_id,
                user_id=user_id,
                parking_lot_id=parking_lot_id,
                start_time=start_time,
                end_time=end_time
            )
            reservation.cost = cost
            
            # Store reservation
            self.reservations[reservation_id] = reservation
            
            # Reserve space in parking lot
            lot.reserve_space(reservation_id)
            
            return {"success": True, "reservation": reservation, "cost": cost}
            
        except Exception as e:
            return {"success": False, "error": f"Error processing reservation: {str(e)}"}
    
    def cancel_reservation(self, reservation_id: str) -> dict:
        """Cancel a reservation"""
        try:
            if reservation_id in self.reservations:
                reservation = self.reservations[reservation_id]
                
                # Release space in parking lot
                lot = self.parking_lots.get(reservation.parking_lot_id)
                if lot:
                    lot.release_space(reservation_id)
                    
                # Update reservation status
                reservation.status = "cancelled"
                
                return {"success": True, "message": f"Reservation {reservation_id} cancelled successfully"}
            else:
                return {"success": False, "error": "Reservation not found"}
                
        except Exception as e:
            return {"success": False, "error": f"Error processing cancellation: {str(e)}"}
    
    def extend_reservation(self, reservation_id: str, new_end_time: datetime) -> dict:
        """Extend a reservation"""
        try:
            if reservation_id in self.reservations:
                reservation = self.reservations[reservation_id]
                
                # Check if the reservation can be extended
                if new_end_time > reservation.end_time:
                    reservation.extend_reservation(new_end_time)
                    return {"success": True, "message": "Reservation extended successfully"}
                else:
                    return {"success": False, "error": "New end time must be after current end time"}
            else:
                return {"success": False, "error": "Reservation not found"}
                
        except Exception as e:
            return {"success": False, "error": f"Error processing extension: {str(e)}"}
    
    def modify_reservation_time(self, reservation_id: str, new_start_time: datetime, new_end_time: datetime) -> dict:
        """Modify reservation time"""
        try:
            if reservation_id in self.reservations:
                reservation = self.reservations[reservation_id]
                
                # Check if the reservation can be modified
                if new_start_time < new_end_time:
                    reservation.modify_reservation_time(new_start_time, new_end_time)
                    return {"success": True, "message": "Reservation modified successfully"}
                else:
                    return {"success": False, "error": "New start time must be before new end time"}
            else:
                return {"success": False, "error": "Reservation not found"}
                
        except Exception as e:
            return {"success": False, "error": f"Error processing modification: {str(e)}"}
    
    def process_payment(self, payment_details: PaymentDetails) -> dict:
        """Process a payment"""
        try:
            if payment_details.validate_payment():
                # In a real system, this would integrate with a payment gateway
                payment_details.status = "completed"
                return {"success": True, "message": "Payment processed successfully"}
            else:
                return {"success": False, "error": "Payment validation failed"}
        except Exception as e:
            return {"success": False, "error": f"Error processing payment: {str(e)}"}


def run_simulation():
    print("=== Parking Management System Simulation ===")
    
    # Initialize the system
    reservation_system = ReservationSystem()
    
    # 1. Check parking availability
    print("\n1. Checking parking availability...")
    user_location = "Near Hotel Mariot"
    available_lots = reservation_system.check_parking_availability(user_location)
    
    if available_lots:
        print(f"Found {len(available_lots)} available parking lots:")
        for lot in available_lots:
            print(f"  - {lot.name}: {lot.available_spaces} spaces available, ${lot.price_per_hour}/hour")
    else:
        print("No available parking lots found.")
    
    # 2. Initiate a reservation
    print("\n2. Initiating reservation...")
    user_id = "user_001"
    parking_lot_id = "lot_001"
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=2)
    
    result = reservation_system.initiate_reservation(user_id, parking_lot_id, start_time, end_time)
    
    if result["success"]:
        reservation = result["reservation"]
        cost = result["cost"]
        print(f"Reservation confirmed! ID: {reservation.id}, Cost: ${cost}")
        print(f"Reservation details: {reservation.start_time} to {reservation.end_time}")
    else:
        print(f"Reservation failed: {result['error']}")
    
    # 3. Cancel reservation
    print("\n3. Canceling reservation...")
    if result["success"]:
        cancel_result = reservation_system.cancel_reservation(reservation.id)
        print(cancel_result["message"] if cancel_result["success"] else f"Cancellation failed: {cancel_result['error']}")
    
    # 4. Try to make a new reservation and then extend it
    print("\n4. Making a new reservation and extending it...")
    result2 = reservation_system.initiate_reservation(user_id, parking_lot_id, start_time, end_time)
    
    if result2["success"]:
        reservation = result2["reservation"]
        print(f"New reservation confirmed! ID: {reservation.id}")
        
        # Extend the reservation
        new_end_time = end_time + timedelta(hours=1)
        extend_result = reservation_system.extend_reservation(reservation.id, new_end_time)
        print(extend_result["message"] if extend_result["success"] else f"Extension failed: {extend_result['error']}")
    
    # 5. Process payment
    print("\n5. Processing payment...")
    payment_details = PaymentDetails(
        id="pay_001",
        reservation_id="res_001",
        amount=20.0,
        card_number="1234567890123456",
        expiry_date="12/25",
        cvv="123"
    )
    
    payment_result = reservation_system.process_payment(payment_details)
    print(payment_result["message"] if payment_result["success"] else f"Payment failed: {payment_result['error']}")
    
    print("\n=== Simulation completed ===")

if __name__ == "__main__":
    run_simulation()