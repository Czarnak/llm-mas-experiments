import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
from typing import Dict
from datetime import datetime

from models.payment import PaymentDetails
from utils.logger import setup_logger


class PaymentProcessorAgent(Agent):
    def __init__(self, jid: str, password: str):
        super().__init__(jid, password)
        self.logger = setup_logger("PaymentProcessorAgent")
        
    async def setup(self):
        self.logger.info("Payment Processor agent is ready")
        
        # Add behaviours
        process_payment_behaviour = ProcessPaymentBehaviour()
        self.add_behaviour(process_payment_behaviour)


class ProcessPaymentBehaviour(CyclicBehaviour):
    async def run(self):
        self.logger = setup_logger("ProcessPaymentBehaviour")
        
        # Wait for incoming message
        msg = await self.receive(timeout=10)
        if msg and msg.get_metadata("subject") == "ProcessPayment":
            self.logger.info(f"Received payment request from {msg.sender}")
            
            try:
                # Extract payment details from the message
                # In a real implementation, this would be more structured
                
                # For now, we'll simulate payment processing
                payment_id = f"pay_{int(datetime.now().timestamp())}"
                
                # Validate payment details (simplified)
                payment_details = PaymentDetails(
                    id=payment_id,
                    reservation_id="res_001",  # This would come from the message
                    amount=20.0,  # This would come from the message
                    card_number="1234567890123456",
                    expiry_date="12/25",
                    cvv="123"
                )
                
                if payment_details.validate_payment():
                    # Process the payment
                    response = Message(to=str(msg.sender),
                                      sender=str(self.agent.jid),
                                      subject="PaymentConfirmation",
                                      body=f"Payment processed successfully. ID: {payment_id}")
                    await self.send(response)
                    self.logger.info("Payment processed successfully")
                else:
                    response = Message(to=str(msg.sender),
                                      sender=str(self.agent.jid),
                                      subject="PaymentConfirmation",
                                      body="Payment validation failed")
                    await self.send(response)
                    self.logger.error("Payment validation failed")
                    
            except Exception as e:
                self.logger.error(f"Error processing payment: {e}")
                response = Message(to=str(msg.sender),
                                  sender=str(self.agent.jid),
                                  subject="PaymentConfirmation",
                                  body="Error processing payment")
                await self.send(response)