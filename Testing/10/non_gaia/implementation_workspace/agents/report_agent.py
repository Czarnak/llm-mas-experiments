from crewai import Agent
from langchain_openai import ChatOpenAI


class ReportAgent(Agent):
    def __init__(self, llm):
        super().__init__(
            role='Report Generator',
            goal='Generate a comprehensive report summarizing all information about the apartment and its area',
            backstory='You are an expert in report writing and data synthesis. '
                      'You specialize in combining information from multiple sources '
                      'into a clear, structured, and comprehensive report.',
            verbose=True,
            allow_delegation=False,
            llm=llm
        )