from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class User(BaseModel):
    id: str = Field(..., description="Unique identifier for the user")
    name: str = Field(..., description="Name of the user")
    email: str = Field(..., description="Email of the user")
    location: str = Field(..., description="Current location of the user")
    
    def __init__(self, id: str, name: str, email: str, location: str):
        super().__init__(id=id, name=name, email=email, location=location)
        
    def update_location(self, new_location: str):
        self.location = new_location