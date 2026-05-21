from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PaymentDetails(BaseModel):
    id: str = Field(..., description="Unique identifier for the payment")
    reservation_id: str = Field(..., description="ID of the reservation being paid")
    amount: float = Field(..., description="Payment amount")
    card_number: str = Field(..., description="Card number")
    expiry_date: str = Field(..., description="Card expiry date")
    cvv: str = Field(..., description="Card CVV")
    status: str = Field("pending", description="Payment status: pending, completed, failed")
    
    def validate_payment(self) -> bool:
        # Simple validation logic
        if (self.card_number and len(self.card_number) >= 13 and
            self.expiry_date and len(self.expiry_date) >= 5 and
            self.cvv and len(self.cvv) >= 3 and
            self.amount > 0):
            return True
        return False