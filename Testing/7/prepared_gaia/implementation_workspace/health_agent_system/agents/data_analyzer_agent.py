from crewai import Agent
from langchain_openai import ChatOpenAI
from typing import List, Dict
import sqlite3
import datetime


class DataAnalyzerAgent(Agent):
    def __init__(self, llm):
        super().__init__(
            role="Data Analyzer Agent",
            goal="Otrzymuje od agenta Chatbota lokalizację, czas, wiadomość użytkownika i zagregowane dane medyczne. Przechowuje dane w bazach danych.",
            backstory="Agent odpowiedzialny za analizę i przechowywanie danych medycznych.",
            verbose=True,
            allow_delegation=False,
            tools=[],
            llm=llm
        )

    def store_detailed_data(self, location: str, timestamp: str, message: str, medical_data: str) -> str:
        # In a real implementation, this would store data in a database
        # For simulation, we'll just return a success message
        return f"Dane zapisane: Lokalizacja={location}, Czas={timestamp}, Wiadomość={message[:50]}..., Dane medyczne={medical_data[:50]}..."

    def extract_medical_information(self, detailed_data: str) -> Dict[str, str]:
        # Simple extraction logic
        return {
            "symptoms": "błęk, kaszel",
            "potential_disease": "grypa",
            "medical_field": "medycyna ogólna"
        }

    def store_extracted_data(self, extracted_data: Dict[str, str], timestamp: str, location: str) -> str:
        # In a real implementation, this would store extracted data in a database
        return f"Wyciąg zapisany: {extracted_data}, Czas={timestamp}, Lokalizacja={location}"
