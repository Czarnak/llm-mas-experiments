from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ResidentialReview(BaseModel):
    id: str = Field(..., description="Unique identifier for the review")
    property_id: str = Field(..., description="Reference to the property being reviewed")
    source: str = Field(..., description="Source of the review (e.g., Google, Yelp, local site)")
    title: str = Field(..., description="Title of the review")
    content: str = Field(..., description="Content of the review")
    rating: Optional[float] = Field(None, description="Rating (1-5 scale)")
    review_date: Optional[datetime] = Field(None, description="Date when the review was posted")
    author: Optional[str] = Field(None, description="Name of the reviewer")
    review_data: Optional[dict] = Field(None, description="Additional review details")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        arbitrary_types_allowed = True