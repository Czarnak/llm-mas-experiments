from crewai import Agent
from textwrap import dedent
from typing import List, Optional
from ..models.parking_lot import ParkingLot
from ..services.parking_lot_service import ParkingLotService


class AvailabilityAgent(Agent):
    def __init__(self, parking_lot_service: ParkingLotService):
        self.parking_lot_service = parking_lot_service
        super().__init__(
            role="Parking Availability Agent",
            goal=dedent("""
                You are responsible for checking real-time availability of parking lots
                and ensuring that reservations can only be made when spots are available.
            """),
            backstory=dedent("""
                You have access to real-time data about parking lot availability and
                can quickly verify if spots are available for reservation. You ensure
                that the system only allows reservations when parking is actually available.
            """),
            verbose=True,
            allow_delegation=False,
            tools=[],
        )

    def check_availability(self, parking_lot_id: str) -> Optional[ParkingLot]:
        """
        Check the availability of a specific parking lot
        """
        return self.parking_lot_service.get_parking_lot(parking_lot_id)

    def get_available_parking_lots(self) -> List[ParkingLot]:
        """
        Get all parking lots that currently have available spots
        """
        return self.parking_lot_service.get_available_parking_lots()