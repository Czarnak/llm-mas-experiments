import asyncio
from agents.user_agent import UserAgent
from agents.llm_processor_agent import LLMProcessorAgent
from agents.health_data_handler_agent import HealthDataHandlerAgent
from agents.health_analyzer_agent import HealthAnalyzerAgent
from agents.health_institution_agent import HealthInstitutionAgent
from agents.recommendation_engine_agent import RecommendationEngineAgent
from agents.system_administration_agent import SystemAdministrationAgent
from agents.monitoring_agent import MonitoringAgent

class HealthSymptomSystem:
    def __init__(self):
        self.agents = {}
        self.openai_api_key = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # In a real system, this would be loaded from environment

    async def start_system(self):
        print("Starting Health Symptom System...")
        
        # Create and start agents
        self.agents["user_agent"] = UserAgent("user_agent@localhost", "password123")
        self.agents["llm_processor"] = LLMProcessorAgent("llm_processor@localhost", "password123", self.openai_api_key)
        self.agents["health_data_handler"] = HealthDataHandlerAgent("health_data_handler@localhost", "password123")
        self.agents["health_analyzer"] = HealthAnalyzerAgent("health_analyzer@localhost", "password123")
        self.agents["health_institution"] = HealthInstitutionAgent("health_institution@localhost", "password123")
        self.agents["recommendation_engine"] = RecommendationEngineAgent("recommendation_engine@localhost", "password123")
        self.agents["system_admin"] = SystemAdministrationAgent("system_admin@localhost", "password123")
        self.agents["monitoring_agent"] = MonitoringAgent("monitoring_agent@localhost", "password123")
        
        # Start all agents
        tasks = []
        for agent_name, agent in self.agents.items():
            task = asyncio.create_task(agent.start())
            tasks.append(task)
            print(f"Started {agent_name}")
            
        # Wait for all agents to start
        await asyncio.gather(*tasks)
        print("All agents started successfully")
        
    async def stop_system(self):
        print("Stopping Health Symptom System...")
        
        # Stop all agents
        tasks = []
        for agent_name, agent in self.agents.items():
            task = asyncio.create_task(agent.stop())
            tasks.append(task)
            print(f"Stopped {agent_name}")
            
        # Wait for all agents to stop
        await asyncio.gather(*tasks)
        print("All agents stopped successfully")

    async def simulate_user_interaction(self):
        """Simulate a user submitting symptoms"""
        print("\n=== Simulating User Interaction ===")
        
        # Get the user agent
        user_agent = self.agents["user_agent"]
        
        # Simulate user submitting symptoms
        symptoms_text = "I have a fever, headache, and cough."
        print(f"User submitting symptoms: {symptoms_text}")
        
        # Submit symptoms through user agent
        await user_agent.submit_symptoms(symptoms_text)
        
        print("User interaction simulation completed")

    async def simulate_system_monitoring(self):
        """Simulate system monitoring"""
        print("\n=== Simulating System Monitoring ===")
        
        # Get the system admin agent
        system_admin = self.agents["system_admin"]
        
        # Initiate system monitoring
        metrics = await system_admin.initiate_system_monitoring()
        print(f"System monitoring initiated. Metrics: {metrics}")
        
        print("System monitoring simulation completed")

async def main():
    # Create system instance
    system = HealthSymptomSystem()
    
    try:
        # Start the system
        await system.start_system()
        
        # Simulate user interaction
        await system.simulate_user_interaction()
        
        # Simulate system monitoring
        await system.simulate_system_monitoring()
        
        # Wait a bit to let messages be processed
        await asyncio.sleep(2)
        
        print("\n=== System Simulation Complete ===")
        
    except Exception as e:
        print(f"Error in main: {e}")
    finally:
        # Stop the system
        await system.stop_system()

if __name__ == "__main__":
    asyncio.run(main())