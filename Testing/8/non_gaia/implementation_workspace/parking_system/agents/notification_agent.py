from crewai import Agent
from textwrap import dedent
from typing import Optional
from ..models.reservation import Reservation


class NotificationAgent(Agent):
    def __init__(self):
        super().__init__(
            role="Notification Agent",
            goal=dedent("""
                You are responsible for sending notifications to users about their parking reservations.
                You handle confirmation messages, reminders, and status updates.
            """),
            backstory=dedent("""
                You ensure that users are kept informed about their reservation status,
                sending confirmation messages when reservations are made, and notifications
                when reservations are modified or canceled.
            """),
            verbose=True,
            allow_delegation=False,
            tools=[],
        )

    def send_confirmation(self, reservation: Reservation) -> bool:
        """
        Send confirmation message to user about their reservation
        """
        # In a real implementation, this would send an actual notification
        # For demo purposes, we'll just print a message
        print(f"✅ Reservation confirmed: {reservation.id} for {reservation.cost} PLN")
        print(f"   Parking Lot: {reservation.parking_lot_id}")
        print(f"   Duration: {reservation.start_time} to {reservation.end_time}")
        return True

    def send_cancellation_notification(self, reservation: Reservation) -> bool:
        """
        Send notification about reservation cancellation
        """
        # In a real implementation, this would send an actual notification
        # For demo purposes, we'll just print a message
        print(f"❌ Reservation cancelled: {reservation.id}")
        print(f"   Refund of {reservation.cost} PLN will be processed")
        return True

    def send_modification_notification(self, reservation: Reservation) -> bool:
        """
        Send notification about reservation modification
        """
        # In a real implementation, this would send an actual notification
        # For demo purposes, we'll just print a message
        print(f"📝 Reservation modified: {reservation.id}")
        print(f"   New duration: {reservation.start_time} to {reservation.end_time}")
        return True

    def send_availability_notification(self, parking_lots: list) -> bool:
        """
        Send notification about available parking lots
        """
        # In a real implementation, this would send an actual notification
        # For demo purposes, we'll just print a message
        print(f"📋 Found {len(parking_lots)} parking lots with available spots:")
        for lot in parking_lots:
            print(f"   - {lot.name}: {lot.available_spots} spots available at {lot.price_per_hour} PLN/hour")
        return True