from crewai import Agent
from langchain_openai import ChatOpenAI
from typing import List


class KnowledgeAgent(Agent):
    def __init__(self, llm, agent_id: int):
        super().__init__(
            role="Knowledge Agent",
            goal="Przeszukuje różne zdefiniowane źródła wiedzy medycznej. Wyciąga dane medyczne na podstawie otrzymanego sparafrazowanego zapytania użytkownika.",
            backstory=f"Agent eksperta wiedzy nr {agent_id} odpowiedzialny za przeszukiwanie baz danych medycznych.",
            verbose=True,
            allow_delegation=False,
            tools=[],
            llm=llm
        )

    def search_medical_knowledge(self, query: str) -> str:
        # In a real implementation, this would query actual medical databases
        # For this simulation, we'll return mock data
        return f"Dane medyczne dla zapytania: '{query}'"
