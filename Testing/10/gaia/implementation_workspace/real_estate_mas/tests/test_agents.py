import pytest
from unittest.mock import Mock, patch
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


class TestPropertySearchAgent:
    def test_search_property_by_address(self):
        agent = PropertySearchAgent()
        property_data = agent.search_property_by_address("123 Main Street, Warsaw")
        
        assert property_data is not None
        assert property_data.id is not None
        assert property_data.address == "123 Main Street, Warsaw"
        assert property_data.city == "Warsaw"
        
    def test_search_property_invalid_address(self):
        agent = PropertySearchAgent()
        
        with pytest.raises(ValueError):
            agent.search_property_by_address("")
            
        with pytest.raises(ValueError):
            agent.search_property_by_address("123")  # Too short


class TestDataCollectionAgent:
    def test_fetch_investment_plans(self):
        agent = DataCollectionAgent()
        property_id = "test-property-id-123"
        
        investment_plan = agent.fetch_investment_plans(property_id)
        
        assert investment_plan is not None
        assert investment_plan.id is not None
        assert investment_plan.property_id == property_id
        assert investment_plan.project_name == "Urban Development Project"
        
    def test_fetch_investment_plans_invalid_id(self):
        agent = DataCollectionAgent()
        
        with pytest.raises(ValueError):
            agent.fetch_investment_plans(None)
            
        with pytest.raises(ValueError):
            agent.fetch_investment_plans("")


class TestReviewAggregationAgent:
    def test_fetch_residential_reviews(self):
        agent = ReviewAggregationAgent()
        property_id = "test-property-id-123"
        
        review = agent.fetch_residential_reviews(property_id)
        
        assert review is not None
        assert review.id is not None
        assert review.property_id == property_id
        assert review.source == "Google Reviews"
        assert review.rating == 4.5
        
    def test_fetch_residential_reviews_invalid_id(self):
        agent = ReviewAggregationAgent()
        
        with pytest.raises(ValueError):
            agent.fetch_residential_reviews(None)
            
        with pytest.raises(ValueError):
            agent.fetch_residential_reviews("")


class TestPriceComparisonAgent:
    def test_compare_property_prices(self):
        agent = PriceComparisonAgent()
        property_id = "test-property-id-123"
        
        comparison = agent.compare_property_prices(property_id)
        
        assert comparison is not None
        assert comparison.id is not None
        assert comparison.property_id == property_id
        assert len(comparison.similar_properties) > 0
        assert comparison.price_comparison is not None
        
    def test_compare_property_prices_invalid_id(self):
        agent = PriceComparisonAgent()
        
        with pytest.raises(ValueError):
            agent.compare_property_prices(None)
            
        with pytest.raises(ValueError):
            agent.compare_property_prices("")


class TestReportGenerationAgent:
    def test_generate_property_report(self):
        agent = ReportGenerationAgent()
        property_id = "test-property-id-123"
        
        # Mock the required data
        mock_investment_plan = InvestmentPlan(
            id="test-investment-id-123",
            property_id=property_id,
            project_name="Test Project",
            description="Test Description",
            location="Test Location",
            status="Active"
        )
        
        mock_review = ResidentialReview(
            id="test-review-id-123",
            property_id=property_id,
            source="Test Source",
            title="Test Review",
            content="Test Content",
            rating=4.0
        )
        
        mock_comparison = PropertyComparison(
            id="test-comparison-id-123",
            property_id=property_id,
            similar_properties=[]
        )
        
        report = agent.generate_property_report(property_id, mock_investment_plan, mock_review, mock_comparison)
        
        assert report is not None
        assert report.id is not None
        assert report.property_id == property_id
        assert report.summary is not None
        
    def test_generate_property_report_invalid_inputs(self):
        agent = ReportGenerationAgent()
        
        with pytest.raises(ValueError):
            agent.generate_property_report(None, None, None, None)


class TestPropertyAnalysisAgent:
    def test_analyze_property_data(self):
        agent = PropertyAnalysisAgent()
        property_id = "test-property-id-123"
        
        # Mock the required data
        mock_investment_plan = InvestmentPlan(
            id="test-investment-id-123",
            property_id=property_id,
            project_name="Test Project",
            description="Test Description",
            location="Test Location",
            status="Active"
        )
        
        mock_review = ResidentialReview(
            id="test-review-id-123",
            property_id=property_id,
            source="Test Source",
            title="Test Review",
            content="Test Content",
            rating=4.0
        )
        
        mock_comparison = PropertyComparison(
            id="test-comparison-id-123",
            property_id=property_id,
            similar_properties=[]
        )
        
        report = agent.analyze_property_data(property_id, mock_investment_plan, mock_review, mock_comparison)
        
        assert report is not None
        assert report.id is not None
        assert report.property_id == property_id
        
    def test_aggregate_data(self):
        agent = PropertyAnalysisAgent()
        property_id = "test-property-id-123"
        
        # Mock the required data
        mock_investment_plan = InvestmentPlan(
            id="test-investment-id-123",
            property_id=property_id,
            project_name="Test Project",
            description="Test Description",
            location="Test Location",
            status="Active"
        )
        
        mock_review = ResidentialReview(
            id="test-review-id-123",
            property_id=property_id,
            source="Test Source",
            title="Test Review",
            content="Test Content",
            rating=4.0
        )
        
        mock_comparison = PropertyComparison(
            id="test-comparison-id-123",
            property_id=property_id,
            similar_properties=[]
        )
        
        report = agent.aggregate_data(property_id, mock_investment_plan, mock_review, mock_comparison)
        
        assert report is not None
        assert report.id is not None
        assert report.property_id == property_id