from langchain_core.tools import tool
from typing import Dict, Any
from models.property_report import PropertyReport
from models.property import RealEstateProperty
from models.investment_plan import InvestmentPlan
from models.residential_review import ResidentialReview
from models.property_comparison import PropertyComparison
from datetime import datetime
import uuid


class ReportGenerationAgent:
    """
    Agent responsible for generating the final property report.
    """
    
    def __init__(self):
        self.name = "ReportGenerationAgent"
        
    @tool
    def generate_property_report(self, property_id: str, investment_plan: InvestmentPlan, 
                               residential_review: ResidentialReview, 
                               property_comparison: PropertyComparison) -> PropertyReport:
        """
        Generate a comprehensive property report based on all collected data.
        
        Args:
            property_id (str): The ID of the property
            investment_plan (InvestmentPlan): Investment plan information
            residential_review (ResidentialReview): Residential review information
            property_comparison (PropertyComparison): Property comparison data
            
        Returns:
            PropertyReport: Final comprehensive report about the property
        """
        # In a real implementation, this would generate a detailed report
        # For this simulation, we'll create a mock report
        
        if not property_id:
            raise ValueError("Property ID is required")
            
        # Generate a unique ID for the report
        report_id = str(uuid.uuid4())
        
        # Create a summary based on all the collected information
        summary = f"Property Report for {property_id}: This property is located in Warsaw and has {property_comparison.property_features['bedrooms']} bedrooms and {property_comparison.property_features['bathrooms']} bathrooms. The property is priced at {property_comparison.price_comparison['current_price']} PLN, which is {property_comparison.price_comparison['price_difference']}% below the average comparable price."
        
        # Mock report content - in a real system this would be more detailed
        mock_content = {
            "property_summary": {
                "address": "123 Main Street, Warsaw",
                "price": 1200000.0,
                "bedrooms": 3,
                "bathrooms": 2,
                "area": 85.0,
                "year_built": 2010
            },
            "investment_plans": {
                "project_name": investment_plan.project_name,
                "description": investment_plan.description,
                "status": investment_plan.status,
                "start_date": investment_plan.start_date.strftime('%Y-%m-%d') if investment_plan.start_date else None,
                "end_date": investment_plan.end_date.strftime('%Y-%m-%d') if investment_plan.end_date else None
            },
            "reviews": {
                "source": residential_review.source,
                "title": residential_review.title,
                "rating": residential_review.rating,
                "content": residential_review.content[:100] + "..."  # Truncate for brevity
            },
            "price_comparison": {
                "current_price": property_comparison.price_comparison["current_price"],
                "avg_comparable_price": property_comparison.price_comparison["avg_comparable_price"],
                "price_difference": property_comparison.price_comparison["price_difference"],
                "market_position": property_comparison.price_comparison["market_position"]
            },
            "market_analysis": {
                "area": property_comparison.market_data["area"],
                "market_trend": property_comparison.market_data["market_trend"],
                "average_price_per_sqm": property_comparison.market_data["average_price_per_sqm"]
            }
        }
        
        # Mock report data
        report_data = {
            "id": report_id,
            "property_id": property_id,
            "summary": summary,
            "investment_plans": [investment_plan.id],
            "reviews": [residential_review.id],
            "comparisons": [property_comparison.id],
            "content": mock_content,
            "generated_at": datetime.now(),
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        return PropertyReport(**report_data)
    
    def get_protocol_name(self) -> str:
        return "GeneratePropertyReport"
    
    def get_protocol_description(self) -> str:
        return "Generates a comprehensive property report based on all collected data"
    
    def get_required_inputs(self) -> list:
        return ["property_id", "investment_plan", "residential_review", "property_comparison"]
    
    def get_outputs(self) -> list:
        return ["PropertyReport"]