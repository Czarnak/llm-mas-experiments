from agentscope.agents import Agent
from agentscope.message import Msg
from typing import List, Dict, Any
from models import (
    ResourceRequest, ResourceOffer, ResourceMatch,
    TransportRoute, RouteUpdate, RoadBlockageReport,
    EmergencyNotification, SpecializedNotification
)
import uuid
from datetime import datetime


class ResourceCoordinatorAgent(Agent):
    """
    Agent responsible for coordinating resource requests, offers, and matching.
    """
    
    def __init__(self, name: str = "ResourceCoordinator"):
        super().__init__(name)
        self.requests = {}
        self.offers = {}
        self.matches = {}
        
    def submit_resource_request(self, request: ResourceRequest) -> ResourceRequest:
        """Submit a resource request"""
        self.requests[request.id] = request
        return request
        
    def submit_resource_offer(self, offer: ResourceOffer) -> ResourceOffer:
        """Submit a resource offer"""
        self.offers[offer.id] = offer
        return offer
        
    def match_resources(self, request_id: str, offer_id: str) -> ResourceMatch:
        """Match a resource request with an offer"""
        request = self.requests.get(request_id)
        offer = self.offers.get(offer_id)
        
        if not request or not offer:
            raise ValueError("Request or offer not found")
            
        # Simple matching logic - match the minimum of requested and available
        matched_quantity = min(request.quantity, offer.quantity)
        
        match = ResourceMatch(
            request_id=request_id,
            offer_id=offer_id,
            matched_quantity=matched_quantity
        )
        
        self.matches[match.id] = match
        
        # Update statuses
        request.status = "matched"
        offer.status = "matched"
        
        return match
        
    def process_resource_match(self, request_id: str, offer_id: str) -> ResourceMatch:
        """Process a resource match"""
        return self.match_resources(request_id, offer_id)


class TransportPlannerAgent(Agent):
    """
    Agent responsible for planning and updating transport routes.
    """
    
    def __init__(self, name: str = "TransportPlanner"):
        super().__init__(name)
        self.routes = {}
        self.route_updates = {}
        self.road_blockages = {}
        
    def plan_transport_route(self, route: TransportRoute) -> TransportRoute:
        """Plan a new transport route"""
        self.routes[route.id] = route
        return route
        
    def update_transport_route(self, update: RouteUpdate) -> TransportRoute:
        """Update an existing transport route"""
        route = self.routes.get(update.route_id)
        if not route:
            raise ValueError("Route not found")
            
        # Update route with new information
        route.waypoints = update.new_route
        route.status = "in_progress"
        
        self.routes[route.id] = route
        self.route_updates[update.id] = update
        
        return route
        
    def process_route_update(self, update: RouteUpdate) -> TransportRoute:
        """Process a route update"""
        return self.update_transport_route(update)
        
    def report_road_blockage(self, report: RoadBlockageReport) -> RouteUpdate:
        """Report a road blockage"""
        self.road_blockages[report.id] = report
        
        # For demonstration, we'll create a simple alternative route
        # In a real system, this would use a routing algorithm
        alternative_route = ["Point A", "Point B", "Point C"]
        
        update = RouteUpdate(
            route_id="route_123",  # This would be dynamic in real system
            reason="road_closure",
            new_route=alternative_route
        )
        
        self.route_updates[update.id] = update
        return update


class NotificationAgent(Agent):
    """
    Agent responsible for sending emergency notifications.
    """
    
    def __init__(self, name: str = "NotificationAgent"):
        super().__init__(name)
        self.notifications = {}
        self.specialized_notifications = {}
        
    def send_emergency_notification(self, notification: EmergencyNotification) -> EmergencyNotification:
        """Send an emergency notification"""
        self.notifications[notification.id] = notification
        print(f"[NOTIFICATION] {notification.message}")
        return notification
        
    def send_specialized_notification(self, notification: SpecializedNotification) -> EmergencyNotification:
        """Send a specialized notification to emergency services"""
        self.specialized_notifications[notification.id] = notification
        
        # Create an emergency notification for the general public
        emergency_notification = EmergencyNotification(
            message=f"Critical situation reported: {notification.critical_info}",
            recipients=["all_users"]
        )
        
        self.notifications[emergency_notification.id] = emergency_notification
        print(f"[SPECIALIZED NOTIFICATION] {notification.critical_info}")
        return emergency_notification