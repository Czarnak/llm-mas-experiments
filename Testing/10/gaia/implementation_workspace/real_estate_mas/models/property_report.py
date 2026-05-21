from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class PropertyReport(BaseModel):
    id: str = Field(..., description="Unique identifier for the report")
    property_id: str = Field(..., description="Reference to the property this report relates to")
    summary: str = Field(..., description="Overall summary of the property and its surroundings")
    investment_plans: Optional[List[str]] = Field(None, description="List of investment plan IDs related to the property")
    reviews: Optional[List[str]] = Field(None, description="List of review IDs related to the property")
    comparisons: Optional[List[str]] = Field(None, description="List of comparison IDs related to the property")
    content: Optional[dict] = Field(None, description="Full content of the report")
    generated_at: datetime = Field(default_factory=datetime.now)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        arbitrary_types_allowed = True