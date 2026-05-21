from crewai_tools import BaseTool
import json


class ReportGenerationTool(BaseTool):
    name: str = "Report Generation Tool"
    description: str = "Generates a comprehensive report summarizing all information about the apartment and its area"

    def _run(self, apartment_info: str, investment_info: str, review_info: str, price_comparison: str) -> str:
        # This tool combines all the information into a comprehensive report
        
        # Parse the input data
        apartment_data = json.loads(apartment_info)
        investment_data = json.loads(investment_info)
        review_data = json.loads(review_info)
        price_data = json.loads(price_comparison)
        
        # Generate comprehensive report
        report = {
            "title": f"Comprehensive Apartment Analysis Report",
            "apartment_details": apartment_data,
            "investment_info": investment_data,
            "review_info": review_data,
            "price_comparison": price_data,
            "summary": {
                "overall_rating": "High",
                "investment_potential": "Good",
                "living_quality": "Good",
                "price_competitiveness": "Competitive"
            }
        }
        
        return json.dumps(report, indent=2)