import unittest
from system_orchestrator import HealthAgentSystem


class TestHealthAgentSystem(unittest.TestCase):
    def setUp(self):
        self.system = HealthAgentSystem()

    def tearDown(self):
        self.system.close_database()

    def test_system_initialization(self):
        """Test that the system initializes correctly"""
        self.assertIsNotNone(self.system)
        self.assertIsNotNone(self.system.chatbot)
        self.assertIsNotNone(self.system.aggregator)
        self.assertIsNotNone(self.system.data_analyzer)
        self.assertEqual(len(self.system.knowledge_agents), 3)
        self.assertIsNotNone(self.system.user)

    def test_anonymize_data(self):
        """Test data anonymization"""
        test_message = "Mam PESEL 12345678901 i błęk"
        result = self.system.chatbot.anonymize_data(test_message)
        self.assertIn("[PESEL]", result)
        self.assertNotIn("12345678901", result)

    def test_validate_user_input(self):
        """Test user input validation"""
        # Valid input
        self.assertTrue(self.system.chatbot.validate_user_input("Mam błęk i kaszel"))
        
        # Invalid input - too short
        self.assertFalse(self.system.chatbot.validate_user_input("Hi"))
        
        # Invalid input - too long
        long_input = "A" * 1001
        self.assertFalse(self.system.chatbot.validate_user_input(long_input))
        
        # Invalid input - nonsensical
        self.assertFalse(self.system.chatbot.validate_user_input("xyz abc qwe"))

    def test_rephrase_request(self):
        """Test request rephrasing"""
        test_message = "Mam błęk i kaszel"
        result = self.system.chatbot.rephrase_request(test_message)
        self.assertIn("Użytkownik opisuje objawy", result)

    def test_database_initialization(self):
        """Test database initialization"""
        # The database should be initialized
        self.assertTrue(hasattr(self.system, 'conn'))
        self.assertTrue(hasattr(self.system, 'cursor'))

    def test_process_user_query(self):
        """Test processing a user query"""
        # This test will run without actually calling OpenAI
        test_message = "Mam błęk i kaszel"
        result = self.system.process_user_query(test_message)
        
        # Should return a response
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)
        
        # Should contain expected elements
        self.assertIn("Twoje objawy zostały przeanalizowane", result)
        self.assertIn("Zalecamy skonsultowanie się z lekarzem", result)


if __name__ == '__main__':
    unittest.main()