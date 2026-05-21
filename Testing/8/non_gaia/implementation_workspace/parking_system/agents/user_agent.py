from crewai import Agent
from textwrap import dedent
from typing import List
from ..models.parking_lot import ParkingLot
from ..models.reservation import ReservationRequest
from ..services.search_service import SearchService


class UserAgent(Agent):
    def __init__(self, search_service: SearchService):
        self.search_service = search_service
        super().__init__(
            role="User Interface Agent",
            goal=dedent("""
                You are the user interface agent for the FindMyParking system. Your primary responsibility is to interact with users,
                understand their requests, and coordinate with other agents to fulfill those requests.
                You handle user inquiries about parking availability, reservations, cancellations, and modifications.
            """),
            backstory=dedent("""
                You are the entry point for all user interactions. You translate user requests into structured commands
                that other agents can understand and execute. You ensure a smooth user experience by providing
                clear responses and handling errors gracefully.
            """),
            verbose=True,
            allow_delegation=False,
            tools=[],
        )

    def find_parking_for_hotel(self, hotel_name: str, location: dict) -> List[ParkingLot]:
        """
        Find parking lots near a hotel
        """
        return self.search_service.find_parking_lots_for_hotel(hotel_name, location)

    def find_nearby_parking(self, location: dict) -> List[ParkingLot]:
        """
        Find parking lots near a location
        """
        return self.search_service.find_nearby_parking_lots(location, radius_km=2.0)