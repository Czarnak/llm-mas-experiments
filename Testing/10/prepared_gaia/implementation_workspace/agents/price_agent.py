from crewai import Agent
from textwrap import dedent


class PriceAgent(Agent):
    def __init__(self, platform_name, **kwargs):
        super().__init__(
            role=f"{platform_name} Prices Handler",
            goal=dedent("""
                Retrieve and compare property prices with similar properties in the area.
            """),
            backstory=dedent("""
                You are a price comparison agent responsible for finding and comparing 
                property prices with similar properties in the area.
                You focus on real estate platforms and price data sources.
            """),
            verbose=True,
            allow_delegation=False,
            **kwargs
        )