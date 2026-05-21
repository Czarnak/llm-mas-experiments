from crewai import Agent
from langchain_openai import ChatOpenAI


class ReviewAgent(Agent):
    def __init__(self, llm):
        super().__init__(
            role='Review and Opinion Analyst',
            goal='Check opinions and reviews of local services in the area from different review platforms',
            backstory='You are an expert in gathering and analyzing online reviews and opinions. '
                      'You specialize in collecting information about local services, businesses, '
                      'and amenities from various review platforms and social media sources.',
            verbose=True,
            allow_delegation=False,
            llm=llm
        )