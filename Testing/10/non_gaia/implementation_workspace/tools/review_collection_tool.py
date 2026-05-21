from crewai_tools import BaseTool
import requests
from bs4 import BeautifulSoup
import json


class ReviewCollectionTool(BaseTool):
    name: str = "Review Collection Tool"
    description: str = "Collects reviews and opinions of local services from different review platforms"

    def _run(self, location: str) -> str:
        # This is a mock implementation - in a real system, this would connect to review platforms
        # or scrape relevant review websites
        
        # Simulate gathering reviews
        mock_response = {
            "location": location,
            "reviews": [
                {
                    "platform": "Google Reviews",
                    "rating": 4.2,
                    "review_count": 120,
                    "top_reviews": [
                        "Great location and convenient for public transport.",
                        "Good management and well-maintained building.",
                        "Quiet neighborhood, good for families."
                    ]
                },
                {
                    "platform": "Facebook Community",
                    "rating": 3.8,
                    "review_count": 85,
                    "top_reviews": [
                        "Nice area with good amenities.",
                        "Some noise from nearby construction.",
                        "Good for young professionals."
                    ]
                },
                {
                    "platform": "Local Forum",
                    "rating": 4.0,
                    "review_count": 65,
                    "top_reviews": [
                        "Very convenient for work and shopping.",
                        "Good variety of restaurants nearby.",
                        "Friendly neighbors and safe area."
                    ]
                }
            ],
            "local_services": [
                {
                    "name": "Central Shopping Mall",
                    "distance": "0.5 km",
                    "rating": 4.3,
                    "category": "Retail"
                },
                {
                    "name": "City Hospital",
                    "distance": "1.2 km",
                    "rating": 4.1,
                    "category": "Healthcare"
                },
                {
                    "name": "Public Library",
                    "distance": "0.8 km",
                    "rating": 4.5,
                    "category": "Education"
                }
            ]
        }
        
        return json.dumps(mock_response, indent=2)