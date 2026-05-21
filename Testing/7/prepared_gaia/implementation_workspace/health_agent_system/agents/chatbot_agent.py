from crewai import Agent
from langchain_openai import ChatOpenAI
from typing import List


class ChatbotAgent(Agent):
    def __init__(self, llm):
        super().__init__(
            role="Chatbot Agent",
            goal="Prowadzi rozmowy z użytkownikiem, uwzględniając historię konwersacji. Zbiera lokalizację, czas i wiadomość użytkownika. Zapewnia anonimizację danych, usuwając ewentualne wrażliwe informacje dostarczone przez użytkownika (np. PESEL). Posiada zabezpieczenie przed wprowadzaniem przez użytkownika nonsensownych informacji. Komunikuje się z innymi agentami w celu uzyskania informacji lub podjęcia działań.",
            backstory="Agent odpowiedzialny za interakcję z użytkownikiem i zarządzanie konwersacją.",
            verbose=True,
            allow_delegation=False,
            tools=[],
            llm=llm
        )

    def anonymize_data(self, message: str) -> str:
        # Simple anonymization - in a real system this would be more sophisticated
        # Remove potential PESel numbers and other sensitive data
        import re
        # Remove common Polish ID patterns (PESEL)
        anonymized = re.sub(r'\b\d{11}\b', '[PESEL]', message)
        # Remove phone numbers
        anonymized = re.sub(r'\b\d{3}-\d{3}-\d{3}\b', '[PHONE]', anonymized)
        return anonymized

    def validate_user_input(self, message: str) -> bool:
        # Basic validation
        if not message or len(message.strip()) < 3:
            return False
        if len(message) > 1000:
            return False
        # Check for nonsensical content
        if any(word in message.lower() for word in ['xyz', 'abc', 'qwe', 'asd']):
            return False
        return True

    def rephrase_request(self, message: str) -> str:
        # Simple rephrasing to make it more structured
        return f"Użytkownik opisuje objawy: {message}"
