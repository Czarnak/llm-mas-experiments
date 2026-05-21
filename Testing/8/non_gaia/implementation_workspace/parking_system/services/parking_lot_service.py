from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
from .database import ParkingLotDB
from ..models.parking_lot import ParkingLot


class ParkingLotService:
    def __init__(self, db: Session):
        self.db = db

    def create_parking_lot(self, parking_lot: ParkingLot) -> ParkingLot:
        db_parking_lot = ParkingLotDB(
            id=parking_lot.id,
            name=parking_lot.name,
            location=str(parking_lot.location),
            total_spots=parking_lot.total_spots,
            available_spots=parking_lot.available_spots,
            price_per_hour=parking_lot.price_per_hour,
            address=parking_lot.address,
            opening_hours=str(parking_lot.opening_hours),
            is_active=parking_lot.is_active
        )
        self.db.add(db_parking_lot)
        self.db.commit()
        self.db.refresh(db_parking_lot)
        return self._db_to_model(db_parking_lot)

    def get_parking_lot(self, parking_lot_id: str) -> Optional[ParkingLot]:
        db_parking_lot = self.db.query(ParkingLotDB).filter(ParkingLotDB.id == parking_lot_id).first()
        if db_parking_lot:
            return self._db_to_model(db_parking_lot)
        return None

    def get_parking_lots(self) -> List[ParkingLot]:
        db_parking_lots = self.db.query(ParkingLotDB).all()
        return [self._db_to_model(db_parking_lot) for db_parking_lot in db_parking_lots]

    def update_parking_lot(self, parking_lot_id: str, parking_lot: ParkingLot) -> Optional[ParkingLot]:
        db_parking_lot = self.db.query(ParkingLotDB).filter(ParkingLotDB.id == parking_lot_id).first()
        if db_parking_lot:
            db_parking_lot.name = parking_lot.name
            db_parking_lot.location = str(parking_lot.location)
            db_parking_lot.total_spots = parking_lot.total_spots
            db_parking_lot.available_spots = parking_lot.available_spots
            db_parking_lot.price_per_hour = parking_lot.price_per_hour
            db_parking_lot.address = parking_lot.address
            db_parking_lot.opening_hours = str(parking_lot.opening_hours)
            db_parking_lot.is_active = parking_lot.is_active
            db_parking_lot.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(db_parking_lot)
            return self._db_to_model(db_parking_lot)
        return None

    def delete_parking_lot(self, parking_lot_id: str) -> bool:
        db_parking_lot = self.db.query(ParkingLotDB).filter(ParkingLotDB.id == parking_lot_id).first()
        if db_parking_lot:
            self.db.delete(db_parking_lot)
            self.db.commit()
            return True
        return False

    def get_available_parking_lots(self) -> List[ParkingLot]:
        db_parking_lots = self.db.query(ParkingLotDB).filter(ParkingLotDB.available_spots > 0, ParkingLotDB.is_active == True).all()
        return [self._db_to_model(db_parking_lot) for db_parking_lot in db_parking_lots]

    def _db_to_model(self, db_parking_lot: ParkingLotDB) -> ParkingLot:
        # Convert string representations back to dictionaries
        import json
        location = json.loads(db_parking_lot.location) if isinstance(db_parking_lot.location, str) else db_parking_lot.location
        opening_hours = json.loads(db_parking_lot.opening_hours) if isinstance(db_parking_lot.opening_hours, str) else db_parking_lot.opening_hours
        
        return ParkingLot(
            id=db_parking_lot.id,
            name=db_parking_lot.name,
            location=location,
            total_spots=db_parking_lot.total_spots,
            available_spots=db_parking_lot.available_spots,
            price_per_hour=db_parking_lot.price_per_hour,
            address=db_parking_lot.address,
            opening_hours=opening_hours,
            is_active=db_parking_lot.is_active
        )

    def update_availability(self, parking_lot_id: str, available_spots: int) -> bool:
        db_parking_lot = self.db.query(ParkingLotDB).filter(ParkingLotDB.id == parking_lot_id).first()
        if db_parking_lot:
            db_parking_lot.available_spots = available_spots
            db_parking_lot.updated_at = datetime.utcnow()
            self.db.commit()
            return True
        return False