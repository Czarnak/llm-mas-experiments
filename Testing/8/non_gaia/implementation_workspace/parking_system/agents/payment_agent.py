from crewai import Agent
from textwrap import dedent
from typing import Optional
from ..models.reservation import Reservation


class PaymentAgent(Agent):
    def __init__(self):
        super().__init__(
            role="Payment Processing Agent",
            goal=dedent("""
                You are responsible for handling all payment-related operations for parking reservations.
                You process payments, handle refunds, and ensure secure transaction processing.
            """),
            backstory=dedent("""
                You specialize in secure payment processing and handle all financial transactions
                related to parking reservations. You ensure that payments are processed correctly
                and that users are charged appropriately.
            """),
            verbose=True,
            allow_delegation=False,
            tools=[],
        )

    def process_payment(self, reservation: Reservation) -> bool:
        """
        Process payment for a reservation (mock implementation)
        """
        # In a real implementation, this would integrate with a payment gateway
        # For demo purposes, we'll just return True
        print(f"Processing payment of {reservation.cost} PLN for reservation {reservation.id}")
        return True

    def refund_payment(self, reservation: Reservation) -> bool:
        """
        Process refund for a canceled reservation (mock implementation)
        """
        # In a real implementation, this would integrate with a payment gateway
        # For demo purposes, we'll just return True
        print(f"Processing refund of {reservation.cost} PLN for reservation {reservation.id}")
        return True

    def validate_payment(self, reservation: Reservation) -> bool:
        """
        Validate payment details for a reservation
        """
        # In a real implementation, this would validate payment details
        # For demo purposes, we'll just return True
        return True
