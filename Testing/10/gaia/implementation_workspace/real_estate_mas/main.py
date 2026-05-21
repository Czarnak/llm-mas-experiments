import asyncio
from typing import Dict, Any
from agents.property_search_agent import PropertySearchAgent
from agents.data_collection_agent import DataCollectionAgent
from agents.review_aggregation_agent import ReviewAggregationAgent
from agents.price_comparison_agent import PriceComparisonAgent
from agents.report_generation_agent import ReportGenerationAgent
from agents.property_analysis_agent import PropertyAnalysisAgent
from models.property import RealEstateProperty
from models.investment_plan import InvestmentPlan
from models.residential_review import ResidentialReview
from models.property_comparison import PropertyComparison
from models.property_report import PropertyReport


class RealEstateMAS:
    """
    Main Multi-Agent System for Real Estate Analysis
    """
    
    def __init__(self):
        self.property_search_agent = PropertySearchAgent()
        self.data_collection_agent = DataCollectionAgent()
        self.review_aggregation_agent = ReviewAggregationAgent()
        self.price_comparison_agent = PriceComparisonAgent()
        self.report_generation_agent = ReportGenerationAgent()
        self.property_analysis_agent = PropertyAnalysisAgent()
        
        # Store data between steps
        self.property_data = None
        self.investment_plan_data = None
        self.review_data = None
        self.comparison_data = None
        self.report_data = None
        
    async def execute_workflow(self, address: str) -> PropertyReport:
        """
        Execute the complete property analysis workflow
        
        Args:
            address (str): The address of the property to analyze
            
        Returns:
            PropertyReport: The final comprehensive report
        """
        print(f"Starting property analysis for address: {address}")
        
        try:
            # Step 1: Search for property by address
            print("Step 1: Searching for property...")
            self.property_data = self.property_search_agent.search_property_by_address(address)
            print(f"Found property: {self.property_data.address} with ID: {self.property_data.id}")
            
            # Step 2: Fetch investment plans
            print("Step 2: Fetching investment plans...")
            self.investment_plan_data = self.data_collection_agent.fetch_investment_plans(self.property_data.id)
            print(f"Retrieved investment plan: {self.investment_plan_data.project_name}")
            
            # Step 3: Fetch residential reviews
            print("Step 3: Fetching residential reviews...")
            self.review_data = self.review_aggregation_agent.fetch_residential_reviews(self.property_data.id)
            print(f"Retrieved review from {self.review_data.source} with rating {self.review_data.rating}")
            
            # Step 4: Compare property prices
            print("Step 4: Comparing property prices...")
            self.comparison_data = self.price_comparison_agent.compare_property_prices(self.property_data.id)
            print(f"Completed price comparison with {len(self.comparison_data.similar_properties)} similar properties")
            
            # Step 5: Analyze property data
            print("Step 5: Analyzing property data...")
            analysis_report = self.property_analysis_agent.analyze_property_data(
                self.property_data.id,
                self.investment_plan_data,
                self.review_data,
                self.comparison_data
            )
            print("Completed property data analysis")
            
            # Step 6: Generate final report
            print("Step 6: Generating final report...")
            self.report_data = self.report_generation_agent.generate_property_report(
                self.property_data.id,
                self.investment_plan_data,
                self.review_data,
                self.comparison_data
            )
            print("Final report generated successfully!")
            
            return self.report_data
            
        except Exception as e:
            print(f"Error during workflow execution: {str(e)}")
            raise
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        Get the current status of the system
        """
        return {
            "property_data": self.property_data.dict() if self.property_data else None,
            "investment_plan_data": self.investment_plan_data.dict() if self.investment_plan_data else None,
            "review_data": self.review_data.dict() if self.review_data else None,
            "comparison_data": self.comparison_data.dict() if self.comparison_data else None,
            "report_data": self.report_data.dict() if self.report_data else None
        }



async def main():
    """
    Main entrypoint to run the real estate multi-agent system
    """
    # Initialize the multi-agent system
    mas = RealEstateMAS()
    
    # Run the workflow with a test address
    test_address = "123 Main Street, Warsaw, Poland"
    
    print("=== Real Estate Multi-Agent System ===")
    print("Initializing system...")
    
    try:
        # Execute the complete workflow
        report = await mas.execute_workflow(test_address)
        
        # Display results
        print("\n=== ANALYSIS RESULTS ===")
        print(f"Report ID: {report.id}")
        print(f"Property ID: {report.property_id}")
        print(f"Summary: {report.summary}")
        
        if report.content:
            print("\nDetailed Content:")
            for key, value in report.content.items():
                print(f"  {key}: {value}")
                
        print("\n=== SYSTEM EXECUTION COMPLETE ===")
        
    except Exception as e:
        print(f"System execution failed: {str(e)}")
        

if __name__ == "__main__":
    asyncio.run(main())