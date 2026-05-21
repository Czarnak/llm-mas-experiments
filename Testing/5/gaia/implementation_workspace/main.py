import asyncio
from agents_new import ResourceCoordinatorAgent, TransportPlannerAgent, NotificationAgent
from models import (
    ResourceRequest, ResourceOffer, ResourceMatch,
    TransportRoute, RouteUpdate, RoadBlockageReport,
    EmergencyNotification, SpecializedNotification
)

async def run_simulation():
    print("=== Crisis Transport Management System Simulation ===\n")
    
    # Initialize agents
    resource_coordinator = ResourceCoordinatorAgent()
    transport_planner = TransportPlannerAgent()
    notification_agent = NotificationAgent()
    
    print("1. Initializing agents...")
    print(f"   - Resource Coordinator: {resource_coordinator.name}")
    print(f"   - Transport Planner: {transport_planner.name}")
    print(f"   - Notification Agent: {notification_agent.name}")
    
    # Step 1: Submit resource requests and offers
    print("\n2. Submitting resource requests and offers...")
    
    # Resource requests
    request1 = ResourceRequest(
        resource_type="medical supplies",
        quantity=50,
        urgency_level="High",
        location="Hospital A"
    )
    
    request2 = ResourceRequest(
        resource_type="food",
        quantity=100,
        urgency_level="Medium",
        location="Shelter B"
    )
    
    # Resource offers
    offer1 = ResourceOffer(
        resource_type="medical supplies",
        quantity=30,
        location="Warehouse X"
    )
    
    offer2 = ResourceOffer(
        resource_type="food",
        quantity=80,
        location="Distribution Center Y"
    )
    
    # Submit requests and offers
    resource_coordinator.submit_resource_request(request1)
    resource_coordinator.submit_resource_request(request2)
    resource_coordinator.submit_resource_offer(offer1)
    resource_coordinator.submit_resource_offer(offer2)
    
    print(f"   - Submitted request: {request1.resource_type} (Qty: {request1.quantity})")
    print(f"   - Submitted request: {request2.resource_type} (Qty: {request2.quantity})")
    print(f"   - Submitted offer: {offer1.resource_type} (Qty: {offer1.quantity})")
    print(f"   - Submitted offer: {offer2.resource_type} (Qty: {offer2.quantity})")
    
    # Step 2: Match resources
    print("\n3. Matching resources...")
    
    # Match the requests with offers
    match1 = resource_coordinator.match_resources(request1.id, offer1.id)
    match2 = resource_coordinator.match_resources(request2.id, offer2.id)
    
    print(f"   - Matched: {request1.resource_type} with {offer1.resource_type}")
    print(f"   - Matched: {request2.resource_type} with {offer2.resource_type}")
    
    # Step 3: Plan transport routes
    print("\n4. Planning transport routes...")
    
    # Plan initial routes
    route1 = TransportRoute(
        waypoints=["Warehouse X", "Hospital A"],
        estimated_time=45
    )
    
    route2 = TransportRoute(
        waypoints=["Distribution Center Y", "Shelter B"],
        estimated_time=60
    )
    
    transport_planner.plan_transport_route(route1)
    transport_planner.plan_transport_route(route2)
    
    print(f"   - Planned route 1: {route1.waypoints}")
    print(f"   - Planned route 2: {route2.waypoints}")
    
    # Step 4: Report road blockage
    print("\n5. Reporting road blockage...")
    
    blockage = RoadBlockageReport(
        location="Highway 10 between points A and B",
        severity="High",
        estimated_duration=120
    )
    
    # Create a route update that references the first route
    update = RouteUpdate(
        route_id=route1.id,
        reason="road_closure",
        new_route=["Point A", "Point B", "Point C"]
    )
    
    print(f"   - Reported road blockage: {blockage.location}")
    print(f"   - Reason: {update.reason}")
    print(f"   - New route: {update.new_route}")
    
    # Step 5: Update routes based on road blockage
    print("\n6. Updating transport routes...")
    
    updated_route1 = transport_planner.update_transport_route(update)
    
    print(f"   - Updated route 1: {updated_route1.waypoints}")
    
    # Step 6: Send notifications
    print("\n7. Sending notifications...")
    
    # Send emergency notification
    emergency_notification = EmergencyNotification(
        message="Road closure on Highway 10. Alternative route provided.",
        recipients=["all_users"]
    )
    
    notification_agent.send_emergency_notification(emergency_notification)
    
    # Send specialized notification
    specialized_notification = SpecializedNotification(
        critical_info="Severe weather warning affecting transport routes.",
        target_authorities=["Police", "Fire Department", "EMS"]
    )
    
    notification_agent.send_specialized_notification(specialized_notification)
    
    print("\n=== Simulation Complete ===")
    
    # Display final state
    print("\nFinal System State:")
    print(f"   - Active Requests: {len(resource_coordinator.requests)}")
    print(f"   - Active Offers: {len(resource_coordinator.offers)}")
    print(f"   - Active Matches: {len(resource_coordinator.matches)}")
    print(f"   - Active Routes: {len(transport_planner.routes)}")
    print(f"   - Active Road Blockages: {len(transport_planner.road_blockages)}")
    print(f"   - Emergency Notifications: {len(notification_agent.notifications)}")
    print(f"   - Specialized Notifications: {len(notification_agent.specialized_notifications)}")

if __name__ == "__main__":
    asyncio.run(run_simulation())