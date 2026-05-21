from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class Request:
    id: str
    requester_id: str
    resource_type: str
    quantity: int
    location: str
    timestamp: datetime = field(default_factory=datetime.now)
    status: str = "pending"

@dataclass
class AvailableMaterials:
    id: str
    provider_id: str
    resource_type: str
    quantity: int
    location: str
    timestamp: datetime = field(default_factory=datetime.now)
    status: str = "available"

@dataclass
class MatchInformation:
    id: str
    request_id: str
    available_materials_id: str
    matched_quantity: int
    timestamp: datetime = field(default_factory=datetime.now)
    status: str = "matched"

@dataclass
class Notification:
    id: str
    recipient_id: str
    message: str
    timestamp: datetime = field(default_factory=datetime.now)
    type: str = "general"

@dataclass
class SpecialNotification:
    id: str
    recipient_id: str
    message: str
    severity: str  # "low", "medium", "high", "critical"
    timestamp: datetime = field(default_factory=datetime.now)
    type: str = "special"

@dataclass
class Route:
    id: str
    match_id: str
    start_location: str
    end_location: str
    waypoints: List[str]
    estimated_time: int  # in minutes
    timestamp: datetime = field(default_factory=datetime.now)
    status: str = "planned"

@dataclass
class OptimizedRoute:
    id: str
    route_id: str
    optimized_waypoints: List[str]
    estimated_time: int  # in minutes
    timestamp: datetime = field(default_factory=datetime.now)
    status: str = "optimized"

@dataclass
class TruckDriverLocation:
    id: str
    driver_id: str
    current_location: str
    timestamp: datetime = field(default_factory=datetime.now)
    status: str = "moving"
