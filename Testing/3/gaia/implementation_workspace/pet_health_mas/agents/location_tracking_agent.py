from agents.base_agent import Agent
from typing import Dict, Any, List
from pydantic import BaseModel


class LocationTrackingAgent(Agent):
    name: str = "LocationTrackingAgent"
    role: str = "LocationTracker"
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Handle collecting location data
        if 'collect_location_data' in data:
            return self._collect_location_data(data)
        
        # Handle recording location
        elif 'record_location' in data:
            return self._record_location(data)
        
        return {}
    
    def _collect_location_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Simulate collecting location data
        print(f"Location Tracker collecting location data")
        return {
            'status': 'data_collected',
            'data': 'location_data_sample',
            'timestamp': data.get('timestamp', 'unknown')
        }
    
    def _record_location(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Simulate recording location
        print(f"Location Tracker recording location")
        return {
            'status': 'location_recorded',
            'data': data.get('location_data', 'unknown'),
            'timestamp': data.get('timestamp', 'unknown')
        }
    
    def get_capabilities(self) -> List[str]:
        return [
            'CollectLocationData',
            'RecordLocation'
        ]
    
    def get_safety_conditions(self) -> List[str]:
        return [
            'UniqueID(Pet) != Null',
            'LocationData != Null'
        ]
    
    def get_liveness_conditions(self) -> str:
        return "(CollectLocationData . RecordLocation)^ω"