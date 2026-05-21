from agents.chatbot_agent import ChatbotAgent
from agents.knowledge_agent import KnowledgeAgent
from agents.aggregator_agent import AggregatorAgent
from agents.data_analyzer_agent import DataAnalyzerAgent
from agents.user_agent import UserAgent
from langchain_openai import ChatOpenAI
from typing import List, Dict
import uuid
import datetime
import sqlite3
import os


class HealthAgentSystem:
    def __init__(self):
        # Initialize LLM
        self.llm = ChatOpenAI(model="gpt-4", temperature=0.3)
        
        # Initialize agents
        self.chatbot = ChatbotAgent(self.llm)
        self.aggregator = AggregatorAgent(self.llm)
        self.data_analyzer = DataAnalyzerAgent(self.llm)
        
        # Create multiple knowledge agents
        self.knowledge_agents = [KnowledgeAgent(self.llm, i) for i in range(3)]
        
        # Initialize user agent
        self.user = UserAgent()
        
        # Initialize database
        self.init_database()

    def init_database(self):
        # Create SQLite database
        self.db_path = "health_system.db"
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        
        # Create tables
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS detailed_data (
                id TEXT PRIMARY KEY,
                location TEXT,
                timestamp TEXT,
                message TEXT,
                medical_data TEXT
            )''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS extracted_data (
                id TEXT PRIMARY KEY,
                symptoms TEXT,
                potential_disease TEXT,
                medical_field TEXT,
                timestamp TEXT,
                location TEXT
            )''')
        
        self.conn.commit()

    def process_user_query(self, user_message: str) -> str:
        print(f"User query: {user_message}")
        
        # Step 1: Anonymize data
        anonymized_message = self.chatbot.anonymize_data(user_message)
        print(f"Anonymized message: {anonymized_message}")
        
        # Step 2: Validate input
        if not self.chatbot.validate_user_input(anonymized_message):
            return "Nieprawidłowe zapytanie. Proszę wprowadzić więcej informacji."
        
        # Step 3: Rephrase request
        rephrased_request = self.chatbot.rephrase_request(anonymized_message)
        print(f"Rephrased request: {rephrased_request}")
        
        # Step 4: Gather knowledge from multiple agents
        knowledge_data_list = []
        for agent in self.knowledge_agents:
            knowledge_data = agent.search_medical_knowledge(rephrased_request)
            knowledge_data_list.append(knowledge_data)
            print(f"Knowledge data from {agent.role}: {knowledge_data}")
        
        # Step 5: Aggregate data
        aggregated_data = self.aggregator.aggregate_data(knowledge_data_list)
        print(f"Aggregated data: {aggregated_data}")
        
        # Step 6: Get user location
        location = self.user.collect_localization()
        print(f"User location: {location}")
        
        # Step 7: Store detailed data
        timestamp = datetime.datetime.now().isoformat()
        data_id = str(uuid.uuid4())
        store_result = self.data_analyzer.store_detailed_data(
            location, timestamp, user_message, aggregated_data
        )
        
        # Store in database
        self.cursor.execute('''
            INSERT INTO detailed_data (id, location, timestamp, message, medical_data)
            VALUES (?, ?, ?, ?, ?)
        ''', (data_id, location, timestamp, user_message, aggregated_data))
        self.conn.commit()
        print(f"Store result: {store_result}")
        
        # Step 8: Extract medical information
        extracted_data = self.data_analyzer.extract_medical_information(aggregated_data)
        print(f"Extracted data: {extracted_data}")
        
        # Step 9: Store extracted data
        store_extracted_result = self.data_analyzer.store_extracted_data(
            extracted_data, timestamp, location
        )
        
        # Store extracted data in database
        self.cursor.execute('''
            INSERT INTO extracted_data (id, symptoms, potential_disease, medical_field, timestamp, location)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (data_id, 
              extracted_data['symptoms'],
              extracted_data['potential_disease'],
              extracted_data['medical_field'],
              timestamp,
              location))
        self.conn.commit()
        print(f"Store extracted result: {store_extracted_result}")
        
        # Step 10: Generate response for user
        response = self.generate_user_response(extracted_data)
        return response

    def generate_user_response(self, extracted_data: Dict[str, str]) -> str:
        return f"\n".join([
            "Twoje objawy zostały przeanalizowane:",
            f"- Objawy: {extracted_data['symptoms']}",
            f"- Potencjalna choroba: {extracted_data['potential_disease']}",
            f"- Dziedzina medycyny: {extracted_data['medical_field']}",
            "",  
            "Zalecamy skonsultowanie się z lekarzem, jeśli objawy się nasilą.",
            "Możesz skorzystać z naszego systemu do znalezienia bliskich placówek medycznych."
        ])

    def get_reports(self) -> List[Dict]:
        # Get reports from database
        self.cursor.execute("SELECT * FROM extracted_data")
        rows = self.cursor.fetchall()
        reports = []
        for row in rows:
            reports.append({
                'id': row[0],
                'symptoms': row[1],
                'potential_disease': row[2],
                'medical_field': row[3],
                'timestamp': row[4],
                'location': row[5]
            })
        return reports

    def get_detailed_report(self, report_id: str) -> Dict:
        # Get detailed report from database
        self.cursor.execute("SELECT * FROM detailed_data WHERE id = ?", (report_id,))
        row = self.cursor.fetchone()
        if row:
            return {
                'id': row[0],
                'location': row[1],
                'timestamp': row[2],
                'message': row[3],
                'medical_data': row[4]
            }
        return None

    def close_database(self):
        self.conn.close()
