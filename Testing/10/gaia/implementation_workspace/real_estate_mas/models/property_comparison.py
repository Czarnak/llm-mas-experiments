from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PropertyComparison(BaseModel):
    id: str = Field(..., description="Unique identifier for the comparison")
    property_id: str = Field(..., description="Reference to the property being compared")
    similar_properties: list = Field(..., description="List of similar properties for comparison")
    price_comparison: Optional[dict] = Field(None, description="Price comparison data")
    property_features: Optional[dict] = Field(None, description="Feature comparison data")
    market_data: Optional[dict] = Field(None, description="Market data for comparison")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        arbitrary_types_allowed = True