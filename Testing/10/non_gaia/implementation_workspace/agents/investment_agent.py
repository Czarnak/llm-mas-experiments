from crewai import Agent
from langchain_openai import ChatOpenAI


class InvestmentAgent(Agent):
    def __init__(self, llm):
        super().__init__(
            role='Investment Information Specialist',
            goal='Gather information about planned investments in the area from various government sources',
            backstory='You are an expert in gathering government data and investment information. '
                      'You specialize in finding information about planned investments, construction '
                      'projects, and development plans in specific geographic areas.',
            verbose=True,
            allow_delegation=False,
            llm=llm
        )