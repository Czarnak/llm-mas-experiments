from crewai import Agent
from langchain_openai import ChatOpenAI


class ApartmentSearchAgent(Agent):
    def __init__(self, llm):
        super().__init__(
            role='Apartment Search Specialist',
            goal='Search for apartments by address and gather basic information about the property',
            backstory='You are an expert in apartment searching and real estate information gathering. '
                      'You specialize in finding apartments based on specific addresses and '
                      'providing initial information about them.',
            verbose=True,
            allow_delegation=False,
            llm=llm
        )