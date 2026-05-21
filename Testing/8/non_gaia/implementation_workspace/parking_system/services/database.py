from sqlalchemy import create_engine, Column, String, Integer, Float, Boolean, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# Create database engine
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./parking_system.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class ParkingLotDB(Base):
    __tablename__ = "parking_lots"
    
    id: str = Column(String, primary_key=True, index=True)
    name: str = Column(String, index=True)
    location: str = Column(JSON)  # Store as JSON string
    total_spots: int = Column(Integer)
    available_spots: int = Column(Integer)
    price_per_hour: float = Column(Float)
    address: str = Column(String)
    opening_hours: str = Column(JSON)  # Store as JSON string
    is_active: bool = Column(Boolean, default=True)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ReservationDB(Base):
    __tablename__ = "reservations"
    
    id: str = Column(String, primary_key=True, index=True)
    user_id: str = Column(String, index=True)
    parking_lot_id: str = Column(String, index=True)
    spot_id: str = Column(String)
    start_time: datetime = Column(DateTime)
    end_time: datetime = Column(DateTime)
    status: str = Column(String, default="confirmed")
    cost: float = Column(Float)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class UserDB(Base):
    __tablename__ = "users"
    
    id: str = Column(String, primary_key=True, index=True)
    name: str = Column(String, index=True)
    email: str = Column(String, unique=True, index=True)
    phone: str = Column(String, nullable=True)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()