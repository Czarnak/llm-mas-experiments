import asyncio
import sys
import os
from datetime import datetime
import logging

# Add current directory to path to import agents
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/system_simulation.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('SystemSimulation')

# Import our custom agents
from agents.person_in_need import PersonInNeedAgent
from agents.helper import HelperAgent
from agents.data_handler import DataHandlerAgent
from agents.notifier import NotifierAgent
from agents.route_planner import RoutePlannerAgent
from agents.truck_driver import TruckDriverAgent
from agents.services import ServicesAgent

# Import core components
from core.database import Database
from core.message_types import Request, AvailableMaterials, MatchInformation, Notification, SpecialNotification, Route, OptimizedRoute, TruckDriverLocation

async def run_simulation():
    logger.info("Starting Crisis Transportation Management Multi-Agent System Simulation")
    logger.info("======================================================")
    
    # Initialize database
    db = Database("test_crisis_transport.db")
    await db.init_db()
    
    # Create agent instances (simulated without actual SPADe framework)
    logger.info("Creating agent instances...")
    
    # Create instances of the agents
    person_in_need = PersonInNeedAgent("person_in_need@localhost", "password123")
    helper = HelperAgent("helper@localhost", "password123")
    data_handler = DataHandlerAgent("data_handler@localhost", "password123")
    notifier = NotifierAgent("notifier@localhost", "password123")
    route_planner = RoutePlannerAgent("route_planner@localhost", "password123")
    truck_driver = TruckDriverAgent("truck_driver@localhost", "password123")
    services = ServicesAgent("services@localhost", "password123")
    
    # Simulate a complete workflow
    logger.info("Simulating crisis transportation workflow...")
    
    # Step 1: PersonInNeed reports need
    logger.info("1. PersonInNeed reports resource need")
    request = Request(
        id="req_001",
        requester_id="person_in_need@localhost",
        resource_type="medicines",
        quantity=10,
        location="Hospital A"
    )
    
    # Store request in database
    await db.add_request(request)
    logger.info(f"   Request stored: {request.id}")
    
    # Step 2: Helper offers materials
    logger.info("2. Helper offers materials")
    materials = AvailableMaterials(
        id="mat_001",
        provider_id="helper@localhost",
        resource_type="medicines",
        quantity=15,
        location="Warehouse B"
    )
    
    # Store materials in database
    await db.add_available_materials(materials)
    logger.info(f"   Available materials stored: {materials.id}")
    
    # Step 3: DataHandler matches request with materials
    logger.info("3. DataHandler matches request with materials")
    match = MatchInformation(
        id="match_001",
        request_id=request.id,
        available_materials_id=materials.id,
        matched_quantity=10
    )
    
    # Store match in database
    await db.add_match(match)
    logger.info(f"   Match created: {match.id}")
    
    # Step 4: Notifier sends notification
    logger.info("4. Notifier sends notification")
    notification = Notification(
        id="notif_001",
        recipient_id="person_in_need@localhost",
        message="Your request for medicines has been matched with available supplies.",
        type="request_update"
    )
    logger.info(f"   Notification sent: {notification.id}")
    
    # Step 5: RoutePlanner creates route
    logger.info("5. RoutePlanner creates route")
    route = Route(
        id="route_001",
        match_id=match.id,
        start_location="Warehouse B",
        end_location="Hospital A",
        waypoints=["Main St", "Oak Ave", "Pine Rd"],
        estimated_time=45
    )
    logger.info(f"   Route created: {route.id}")
    
    # Step 6: TruckDriver provides location updates
    logger.info("6. TruckDriver provides location updates")
    location = TruckDriverLocation(
        id="loc_001",
        driver_id="truck_driver@localhost",
        current_location="On route to Hospital A"
    )
    logger.info(f"   Location update: {location.id}")
    
    # Step 7: Services receives special notification
    logger.info("7. Services receives special notification")
    special_notification = SpecialNotification(
        id="spec_notif_001",
        recipient_id="services@localhost",
        message="Road closure detected on Main Street due to flooding.",
        severity="high"
    )
    logger.info(f"   Special notification sent: {special_notification.id}")
    
    logger.info("\nWorkflow simulation completed successfully!")
    logger.info("======================================================")
    
    # Show final database state
    logger.info("Final database state:")
    requests = await db.get_requests()
    materials = await db.get_available_materials()
    matches = await db.get_matches()
    
    logger.info(f"Requests: {len(requests)}")
    logger.info(f"Available Materials: {len(materials)}")
    logger.info(f"Matches: {len(matches)}")

async def main():
    try:
        await run_simulation()
        logger.info("\nSystem simulation completed successfully!")
    except Exception as e:
        logger.error(f"Error during simulation: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())