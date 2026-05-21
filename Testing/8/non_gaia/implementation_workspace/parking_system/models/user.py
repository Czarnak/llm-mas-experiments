from pydantic import BaseModel, Field
from typing import Optional


class User(BaseModel):
    id: str = Field(..., description="Unique identifier for the user")
    name: str = Field(..., description="User's name")
    email: str = Field(..., description="User's email")
    phone: Optional[str] = Field(None, description="User's phone number")
    
    class Config:
        schema_extra = {
            "example": {
                "id": "user_123",
                "name": "Jan Kowalski",
                "email": "jan.kowalski@example.com",
                "phone": "+48 123 456 789"
            }
        }