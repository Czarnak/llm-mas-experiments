from pydantic import BaseModel, Field
from typing import Optional, List
import uuid
from datetime import datetime


class ResourceRequest(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    resource_type: str
    quantity: int
    urgency_level: str  # Low, Medium, High, Critical
    location: str
    timestamp: datetime = Field(default_factory=datetime.now)
    status: str = "pending"  # pending, matched, fulfilled


class ResourceOffer(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    resource_type: str
    quantity: int
    location: str
    timestamp: datetime = Field(default_factory=datetime.now)
    status: str = "available"  # available, matched, fulfilled


class ResourceMatch(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    request_id: str
    offer_id: str
    matched_quantity: int
    timestamp: datetime = Field(default_factory=datetime.now)
    status: str = "active"  # active, completed, cancelled


class TransportRoute(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    waypoints: List[str]
    estimated_time: int  # in minutes
    status: str = "planned"  # planned, in_progress, completed, cancelled
    current_location: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)


class RouteUpdate(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    route_id: str
    reason: str  # "accident", "road_closure", "weather", "other"
    new_route: List[str]
    timestamp: datetime = Field(default_factory=datetime.now)


class RoadBlockageReport(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    location: str
    severity: str  # Low, Medium, High, Critical
    estimated_duration: int  # in minutes
    timestamp: datetime = Field(default_factory=datetime.now)
    status: str = "reported"  # reported, acknowledged, resolved


class EmergencyNotification(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    message: str
    recipients: List[str]
    timestamp: datetime = Field(default_factory=datetime.now)
    priority: str = "normal"  # normal, high, critical


class SpecializedNotification(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    critical_info: str
    target_authorities: List[str]
    timestamp: datetime = Field(default_factory=datetime.now)
