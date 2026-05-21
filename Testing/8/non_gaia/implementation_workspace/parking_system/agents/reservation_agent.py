from crewai import Agent
from textwrap import dedent
from typing import Optional
from ..models.reservation import Reservation, ReservationRequest
from ..services.reservation_service import ReservationService


class ReservationAgent(Agent):
    def __init__(self, reservation_service: ReservationService):
        self.reservation_service = reservation_service
        super().__init__(
            role="Reservation Management Agent",
            goal=dedent("""
                You are responsible for managing all parking reservations including creating,
                modifying, and canceling reservations. You ensure that reservations are
                valid and follow all business rules.
            """),
            backstory=dedent("""
                You handle all reservation-related operations with precision and accuracy.
                You verify that reservations are valid, check availability, and ensure
                proper handling of reservation modifications and cancellations.
            """),
            verbose=True,
            allow_delegation=False,
            tools=[],
        )

    def create_reservation(self, reservation_request: ReservationRequest) -> Optional[Reservation]:
        """
        Create a new parking reservation
        """
        return self.reservation_service.create_reservation(reservation_request)

    def cancel_reservation(self, reservation_id: str) -> bool:
        """
        Cancel an existing reservation
        """
        return self.reservation_service.cancel_reservation(reservation_id)

    def extend_reservation(self, reservation_id: str, new_end_time: str) -> Optional[Reservation]:
        """
        Extend an existing reservation
        """
        # In a real implementation, this would parse the datetime string
        # For now, we'll just return None as this is a demo
        return self.reservation_service.extend_reservation(reservation_id, new_end_time)

    def modify_reservation(self, reservation_id: str, new_start_time: str, new_end_time: str) -> Optional[Reservation]:
        """
        Modify an existing reservation
        """
        # In a real implementation, this would parse the datetime strings
        # For now, we'll just return None as this is a demo
        return self.reservation_service.modify_reservation(reservation_id, new_start_time, new_end_time)

    def get_reservation(self, reservation_id: str) -> Optional[Reservation]:
        """
        Get details of a specific reservation
        """
        return self.reservation_service.get_reservation(reservation_id)