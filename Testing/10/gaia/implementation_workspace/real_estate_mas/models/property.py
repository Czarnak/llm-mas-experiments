from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class RealEstateProperty(BaseModel):
    id: str = Field(..., description="Unique identifier for the property")
    address: str = Field(..., description="Full address of the property")
    city: str = Field(..., description="City where the property is located")
    postal_code: str = Field(..., description="Postal code of the property")
    latitude: Optional[float] = Field(None, description="Latitude coordinate")
    longitude: Optional[float] = Field(None, description="Longitude coordinate")
    property_type: str = Field(..., description="Type of property (apartment, house, etc.)")
    price: Optional[float] = Field(None, description="Current price of the property")
    bedrooms: Optional[int] = Field(None, description="Number of bedrooms")
    bathrooms: Optional[int] = Field(None, description="Number of bathrooms")
    area: Optional[float] = Field(None, description="Area in square meters")
    year_built: Optional[int] = Field(None, description="Year the property was built")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        arbitrary_types_allowed = True