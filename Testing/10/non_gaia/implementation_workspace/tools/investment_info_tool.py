from crewai_tools import BaseTool
import requests
from bs4 import BeautifulSoup
import json


class InvestmentInfoTool(BaseTool):
    name: str = "Investment Information Tool"
    description: str = "Gathers information about planned investments in the area from various government sources"

    def _run(self, location: str) -> str:
        # This is a mock implementation - in a real system, this would connect to government databases
        # or scrape relevant government websites
        
        # Simulate gathering investment data
        mock_response = {
            "location": location,
            "planned_investments": [
                {
                    "project_name": "Urban Development Project",
                    "description": "New residential complex with commercial spaces",
                    "estimated_investment": "50000000",
                    "status": "planning",
                    "expected_completion": "2026"
                },
                {
                    "project_name": "Transport Infrastructure",
                    "description": "New metro line extension",
                    "estimated_investment": "150000000",
                    "status": "under_construction",
                    "expected_completion": "2025"
                }
            ],
            "development_projects": [
                {
                    "project_name": "City Park Renovation",
                    "description": "Renovation of central park with new playgrounds and facilities",
                    "estimated_investment": "20000000",
                    "status": "approved",
                    "expected_completion": "2024"
                }
            ]
        }
        
        return json.dumps(mock_response, indent=2)