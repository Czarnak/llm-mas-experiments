from crewai import Agent
from textwrap import dedent
from typing import List
from ..models.parking_lot import ParkingLot
from ..services.search_service import SearchService


class ParkingSearchAgent(Agent):
    def __init__(self, search_service: SearchService):
        self.search_service = search_service
        super().__init__(
            role="Parking Search Agent",
            goal=dedent("""
                You are responsible for finding and recommending parking lots based on user location and requirements.
                You search for parking lots within a 2km radius and provide recommendations sorted by price.
            """),
            backstory=dedent("""
                You have extensive knowledge of parking lot locations and can quickly find the best options
                for users based on their location and requirements. You ensure that the recommendations
                are accurate and sorted by cost for optimal user experience.
            """),
            verbose=True,
            allow_delegation=False,
            tools=[],
        )

    def find_nearby_parking(self, location: dict) -> List[ParkingLot]:
        """
        Find parking lots near a location within 2km radius
        """
        return self.search_service.find_nearby_parking_lots(location, radius_km=2.0)

    def find_parking_for_hotel(self, hotel_name: str, location: dict) -> List[ParkingLot]:
        """
        Find parking lots near a hotel
        """
        return self.search_service.find_parking_lots_for_hotel(hotel_name, location)