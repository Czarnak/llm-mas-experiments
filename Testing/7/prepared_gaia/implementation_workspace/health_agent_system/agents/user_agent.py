from typing import Dict, List


class UserAgent:
    def __init__(self):
        self.name = "User Agent"
        self.location = "Warsaw, Poland"
        self.history = []

    def collect_localization(self) -> str:
        return self.location

    def ask(self, message: str) -> str:
        # Simulate user asking a question
        return message

    def receive_message(self, message: str) -> None:
        # Simulate receiving a response
        print(f"User received: {message}")
        self.history.append(message)
