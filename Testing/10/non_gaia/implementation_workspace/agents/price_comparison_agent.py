from crewai import Agent
from langchain_openai import ChatOpenAI


class PriceComparisonAgent(Agent):
    def __init__(self, llm):
        super().__init__(
            role='Price Comparison Specialist',
            goal='Compare apartment prices with similar properties in the area from various real estate platforms',
            backstory='You are an expert in real estate market analysis and price comparison. '
                      'You specialize in finding comparable properties, analyzing market trends, '
                      'and providing price comparisons for apartments in specific areas.',
            verbose=True,
            allow_delegation=False,
            llm=llm
        )