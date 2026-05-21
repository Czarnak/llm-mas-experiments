from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class InvestmentPlan(BaseModel):
    id: str = Field(..., description="Unique identifier for the investment plan")
    property_id: str = Field(..., description="Reference to the property this plan relates to")
    project_name: str = Field(..., description="Name of the investment project")
    description: str = Field(..., description="Description of the investment project")
    location: str = Field(..., description="Location where the investment will take place")
    start_date: Optional[datetime] = Field(None, description="Start date of the investment")
    end_date: Optional[datetime] = Field(None, description="End date of the investment")
    status: str = Field(..., description="Status of the investment project")
    project_data: Optional[dict] = Field(None, description="Additional project details")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        arbitrary_types_allowed = True