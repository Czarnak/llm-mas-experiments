from crewai import Agent
from textwrap import dedent


class CustomerAgent(Agent):
    def __init__(self, **kwargs):
        super().__init__(
            role="Customer",
            goal=dedent("""
                Provide the address of the property for analysis and receive the final report.
            """),
            backstory=dedent("""
                You are the customer who wants to analyze a property. 
                You provide the address of the property and expect a comprehensive report.
            """),
            verbose=True,
            allow_delegation=False,
            **kwargs
        )