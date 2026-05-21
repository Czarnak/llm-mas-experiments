import os
from dotenv import load_dotenv
from crewai import Task, Process, Crew
from langchain_openai import ChatOpenAI

# Import agents
from agents.apartment_search_agent import ApartmentSearchAgent
from agents.investment_agent import InvestmentAgent
from agents.review_agent import ReviewAgent
from agents.price_comparison_agent import PriceComparisonAgent
from agents.report_agent import ReportAgent

# Import tools
from tools.apartment_search_tool import ApartmentSearchTool
from tools.investment_info_tool import InvestmentInfoTool
from tools.review_collection_tool import ReviewCollectionTool
from tools.price_comparison_tool import PriceComparisonTool
from tools.report_generation_tool import ReportGenerationTool

# Load environment variables
load_dotenv()

class ApartmentAnalysisSystem:
    def __init__(self):
        # Check if API key is set
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "sk-...your-api-key-here...":
            raise ValueError("OPENAI_API_KEY environment variable is not set or is the placeholder value.")
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            model="gpt-4-turbo",
            temperature=0.7,
            api_key=api_key
        )
        
        # Create agents
        self.apartment_search_agent = ApartmentSearchAgent(self.llm)
        self.investment_agent = InvestmentAgent(self.llm)
        self.review_agent = ReviewAgent(self.llm)
        self.price_comparison_agent = PriceComparisonAgent(self.llm)
        self.report_agent = ReportAgent(self.llm)
        
        # Create tools
        self.apartment_search_tool = ApartmentSearchTool()
        self.investment_info_tool = InvestmentInfoTool()
        self.review_collection_tool = ReviewCollectionTool()
        self.price_comparison_tool = PriceComparisonTool()
        self.report_generation_tool = ReportGenerationTool()
        
        # Assign tools to agents
        self.apartment_search_agent.tools = [self.apartment_search_tool]
        self.investment_agent.tools = [self.investment_info_tool]
        self.review_agent.tools = [self.review_collection_tool]
        self.price_comparison_agent.tools = [self.price_comparison_tool]
        self.report_agent.tools = [self.report_generation_tool]
        
    def run_analysis(self, address: str):
        # Task 1: Search for apartment by address
        search_task = Task(
            description=f"Search for apartment at address: {address}",
            agent=self.apartment_search_agent,
            expected_output="Detailed information about the apartment including price, size, rooms, floor, etc."
        )
        
        # Task 2: Gather investment information
        investment_task = Task(
            description=f"Gather information about planned investments in the area of {address}",
            agent=self.investment_agent,
            expected_output="Information about planned investments, construction projects, and development plans in the area"
        )
        
        # Task 3: Collect reviews and opinions
        review_task = Task(
            description=f"Collect reviews and opinions of local services in the area around {address}",
            agent=self.review_agent,
            expected_output="Reviews and opinions from various platforms about local services and amenities"
        )
        
        # Task 4: Compare prices with similar properties
        price_comparison_task = Task(
            description=f"Compare the apartment at {address} with similar properties in the area",
            agent=self.price_comparison_agent,
            expected_output="Price comparison with similar apartments including price per square meter and distances"
        )
        
        # Task 5: Generate comprehensive report
        report_task = Task(
            description="Generate a comprehensive report summarizing all information about the apartment and its area",
            agent=self.report_agent,
            expected_output="A complete report with apartment details, investment info, reviews, price comparison, and summary"
        )
        
        # Create crew
        crew = Crew(
            agents=[
                self.apartment_search_agent,
                self.investment_agent,
                self.review_agent,
                self.price_comparison_agent,
                self.report_agent
            ],
            tasks=[
                search_task,
                investment_task,
                review_task,
                price_comparison_task,
                report_task
            ],
            process=Process.sequential,
            verbose=True
        )
        
        # Execute the crew
        result = crew.kickoff()
        
        return result

# Main execution
if __name__ == "__main__":
    # Initialize the system
    try:
        system = ApartmentAnalysisSystem()
    except ValueError as e:
        print(f"Error initializing system: {str(e)}")
        print("Please set the OPENAI_API_KEY environment variable in .env file.")
        exit(1)
    
    # Run analysis for a sample address
    sample_address = "123 Main Street, Warsaw, Poland"
    print(f"Starting apartment analysis for: {sample_address}")
    
    try:
        result = system.run_analysis(sample_address)
        print("\nAnalysis completed successfully!")
        print("\nResult:", result)
    except Exception as e:
        print(f"Error during analysis: {str(e)}")