from crewai import Task
from textwrap import dedent


class RealEstateTasks:
    
    @staticmethod
    def customer_task(agent):
        return Task(
            description=dedent("""
                Provide the address of the property for analysis.
                Example address: "ul. Warszawska 15, Warszawa, Poland"
            """),
            expected_output=dedent("""
                A clear property address in a standardized format.
            """),
            agent=agent
        )
    
    @staticmethod
    def department_task(agent, property_address):
        return Task(
            description=dedent(f"""
                Research planned investments and developments in the area around {property_address}.
                Focus on official government sources and urban planning information.
                Look for information about new schools, buildings, commercial developments, 
                infrastructure projects, and public services.
            """),
            expected_output=dedent("""
                A summary of planned investments and developments in the area including:
                - New construction projects
                - Planned infrastructure improvements
                - Public service developments
                - Urban planning initiatives
            """),
            agent=agent
        )
    
    @staticmethod
    def opinion_task(agent, property_address):
        return Task(
            description=dedent(f"""
                Gather opinions and reviews about local services and amenities around {property_address}.
                Focus on restaurants, shops, entertainment venues, and other local services.
                Collect reviews from various platforms.
            """),
            expected_output=dedent("""
                A summary of local opinions and reviews including:
                - Restaurant reviews
                - Shop ratings
                - Entertainment venue feedback
                - Overall local service quality
            """),
            agent=agent
        )
    
    @staticmethod
    def price_task(agent, property_address):
        return Task(
            description=dedent(f"""
                Compare property prices with similar properties around {property_address}.
                Focus on similar properties in terms of size, location, age, and amenities.
            """),
            expected_output=dedent("""
                A price comparison report including:
                - Average price per square meter in the area
                - Similar property prices
                - Price trends
                - Market value assessment
            """),
            agent=agent
        )
    
    @staticmethod
    def reporter_task(agent, *context_tasks):
        return Task(
            description=dedent("""
                Compile all the information from the specialized agents into a comprehensive report.
                Create a structured report that includes investment information, local opinions, 
                and price comparisons.
            """),
            expected_output=dedent("""
                A final comprehensive report including:
                - Investment and development information
                - Local service opinions and reviews
                - Price comparison with similar properties
                - Overall property assessment
            """),
            agent=agent,
            context=list(context_tasks)
        )