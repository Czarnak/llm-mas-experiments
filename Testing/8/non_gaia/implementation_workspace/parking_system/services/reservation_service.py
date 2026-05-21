from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
from ..models.reservation import Reservation, ReservationRequest
from .database import ReservationDB
from .parking_lot_service import ParkingLotService


class ReservationService:
    def __init__(self, db: Session, parking_lot_service: ParkingLotService):
        self.db = db
        self.parking_lot_service = parking_lot_service

    def create_reservation(self, reservation_request: ReservationRequest) -> Optional[Reservation]:
        # Check if parking lot exists and has available spots
        parking_lot = self.parking_lot_service.get_parking_lot(reservation_request.parking_lot_id)
        if not parking_lot or parking_lot.available_spots <= 0:
            return None
        
        # Check if the requested time is in the future
        if reservation_request.start_time <= datetime.utcnow():
            return None
        
        # Calculate cost
        duration_hours = (reservation_request.end_time - reservation_request.start_time).total_seconds() / 3600
        cost = duration_hours * parking_lot.price_per_hour
        
        # Create reservation
        reservation = Reservation(
            id=f"res_{len(self.get_reservations()) + 1}",
            user_id=reservation_request.user_id,
            parking_lot_id=reservation_request.parking_lot_id,
            spot_id=f"spot_{len(self.get_reservations()) + 1}",  # Simplified for demo
            start_time=reservation_request.start_time,
            end_time=reservation_request.end_time,
            cost=cost,
            created_at=datetime.utcnow()
        )
        
        # Save to database
        db_reservation = ReservationDB(
            id=reservation.id,
            user_id=reservation.user_id,
            parking_lot_id=reservation.parking_lot_id,
            spot_id=reservation.spot_id,
            start_time=reservation.start_time,
            end_time=reservation.end_time,
            status=reservation.status,
            cost=reservation.cost,
            created_at=reservation.created_at
        )
        
        self.db.add(db_reservation)
        self.db.commit()
        self.db.refresh(db_reservation)
        
        # Update parking lot availability
        new_available_spots = parking_lot.available_spots - 1
        self.parking_lot_service.update_availability(reservation.parking_lot_id, new_available_spots)
        
        return reservation

    def get_reservation(self, reservation_id: str) -> Optional[Reservation]:
        db_reservation = self.db.query(ReservationDB).filter(ReservationDB.id == reservation_id).first()
        if db_reservation:
            return self._db_to_model(db_reservation)
        return None

    def get_reservations(self) -> List[Reservation]:
        db_reservations = self.db.query(ReservationDB).all()
        return [self._db_to_model(db_reservation) for db_reservation in db_reservations]

    def cancel_reservation(self, reservation_id: str) -> bool:
        db_reservation = self.db.query(ReservationDB).filter(ReservationDB.id == reservation_id).first()
        if db_reservation:
            # Update reservation status
            db_reservation.status = "cancelled"
            db_reservation.updated_at = datetime.utcnow()
            self.db.commit()
            
            # Update parking lot availability (revert the spot)
            reservation = self._db_to_model(db_reservation)
            parking_lot = self.parking_lot_service.get_parking_lot(reservation.parking_lot_id)
            if parking_lot:
                new_available_spots = parking_lot.available_spots + 1
                self.parking_lot_service.update_availability(reservation.parking_lot_id, new_available_spots)
            
            return True
        return False

    def extend_reservation(self, reservation_id: str, new_end_time: datetime) -> Optional[Reservation]:
        reservation = self.get_reservation(reservation_id)
        if not reservation:
            return None
        
        # Check if the new end time is in the future
        if new_end_time <= datetime.utcnow():
            return None
        
        # Check if the parking lot still has availability
        parking_lot = self.parking_lot_service.get_parking_lot(reservation.parking_lot_id)
        if not parking_lot or parking_lot.available_spots < 0:  # Simplified for demo
            return None
        
        # Update reservation
        db_reservation = self.db.query(ReservationDB).filter(ReservationDB.id == reservation_id).first()
        db_reservation.end_time = new_end_time
        db_reservation.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(db_reservation)
        
        # Recalculate cost
        duration_hours = (new_end_time - reservation.start_time).total_seconds() / 3600
        new_cost = duration_hours * parking_lot.price_per_hour
        db_reservation.cost = new_cost
        self.db.commit()
        
        return self._db_to_model(db_reservation)

    def modify_reservation(self, reservation_id: str, new_start_time: datetime, new_end_time: datetime) -> Optional[Reservation]:
        reservation = self.get_reservation(reservation_id)
        if not reservation:
            return None
        
        # Check if the new times are in the future
        if new_start_time <= datetime.utcnow() or new_end_time <= datetime.utcnow():
            return None
        
        # Check if the parking lot still has availability
        parking_lot = self.parking_lot_service.get_parking_lot(reservation.parking_lot_id)
        if not parking_lot or parking_lot.available_spots < 0:  # Simplified for demo
            return None
        
        # Update reservation
        db_reservation = self.db.query(ReservationDB).filter(ReservationDB.id == reservation_id).first()
        db_reservation.start_time = new_start_time
        db_reservation.end_time = new_end_time
        db_reservation.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(db_reservation)
        
        # Recalculate cost
        duration_hours = (new_end_time - new_start_time).total_seconds() / 3600
        new_cost = duration_hours * parking_lot.price_per_hour
        db_reservation.cost = new_cost
        self.db.commit()
        
        return self._db_to_model(db_reservation)

    def _db_to_model(self, db_reservation: ReservationDB) -> Reservation:
        return Reservation(
            id=db_reservation.id,
            user_id=db_reservation.user_id,
            parking_lot_id=db_reservation.parking_lot_id,
            spot_id=db_reservation.spot_id,
            start_time=db_reservation.start_time,
            end_time=db_reservation.end_time,
            status=db_reservation.status,
            cost=db_reservation.cost,
            created_at=db_reservation.created_at
        )