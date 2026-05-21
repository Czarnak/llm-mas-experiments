from crewai import Agent
from pydantic import BaseModel
from typing import List, Dict, Any


class RoutePlannerAgent:
    def __init__(self):
        self.role = "Route Planner"
        self.goal = "Plan optimal transportation routes and provide alternative routes"
        self.backstory = "An agent responsible for planning the most efficient transportation routes, considering traffic conditions, road closures, and alternative paths."
        self.tools = []

    def create_agent(self):
        return Agent(
            role=self.role,
            goal=self.goal,
            backstory=self.backstory,
            verbose=True,
            allow_delegation=False,
            tools=self.tools,
            max_iter=5,
            memory=True
        )

    def plan_route(self, start_location: str, end_location: str, waypoints: List[str] = None) -> Dict[str, Any]:
        """Plan the optimal route from start to end location"""
        # Simulated route planning
        route_details = {
            "start": start_location,
            "end": end_location,
            "waypoints": waypoints or [],
            "route_id": "route_001",
            "distance": "15.2 km",
            "estimated_time": "25 minutes",
            "traffic_conditions": "moderate",
            "status": "planned"
        }
        
        print(f"Route Planned: {start_location} to {end_location}")
        print(f"Estimated time: {route_details['estimated_time']}")
        return route_details

    def find_alternative_routes(self, current_route: Dict[str, Any], incident: str) -> List[Dict[str, Any]]:
        """Find alternative routes in case of incidents"""
        # Simulated alternative routes
        alternative_routes = [
            {
                "route_id": "alt_route_001",
                "distance": "18.5 km",
                "estimated_time": "35 minutes",
                "reason": f"Avoiding {incident}"
            },
            {
                "route_id": "alt_route_002",
                "distance": "16.8 km",
                "estimated_time": "30 minutes",
                "reason": f"Alternative path due to {incident}"
            }
        ]
        
        print(f"Alternative routes found for incident: {incident}")
        return alternative_routes

    def update_route(self, route_id: str, new_conditions: Dict[str, Any]) -> Dict[str, Any]:
        """Update route based on new conditions"""
        updated_route = {
            "route_id": route_id,
            "status": "updated",
            "new_conditions": new_conditions,
            "updated_time": "2023-05-15 14:30:00"
        }
        
        print(f"Route {route_id} updated due to new conditions")
        return updated_route