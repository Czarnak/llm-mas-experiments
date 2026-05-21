from crewai import Agent
from langchain_openai import ChatOpenAI
from typing import List


class AggregatorAgent(Agent):
    def __init__(self, llm):
        super().__init__(
            role="Aggregator Agent",
            goal="Agreguje dane z różnych źródeł od agentów Wiedzy. Tworzy spójną informację medyczną.",
            backstory="Agent odpowiedzialny za agregację danych medycznych z wielu źródeł.",
            verbose=True,
            allow_delegation=False,
            tools=[],
            llm=llm
        )

    def aggregate_data(self, knowledge_data_list: List[str]) -> str:
        # Simple aggregation logic
        aggregated = "\n".join(knowledge_data_list)
        return f"Zagregowane dane:\n{aggregated}"
