import asyncio
from typing import Dict, List
from agents.coordinator_agent import CoordinatorAgent
from agents.reception_agent import ReceptionAgent
from agents.adoption_agent import AdoptionAgent
from agents.worker_agent import WorkerAgent
from agents.room_agent import RoomAgent
from agents.animal_assistant_agent import AnimalAssistantAgent
from agents.applicant_agent import ApplicantAgent
from services.service_layer import ServiceLayer


class MultiAgentSystem:
    def __init__(self):
        self.agents = {}
        self.service_layer = ServiceLayer()
        self.setup_agents()

    def setup_agents(self):
        # Create coordinator agent
        self.agents['coordinator'] = CoordinatorAgent("coordinator")
        
        # Create reception agent
        self.agents['reception'] = ReceptionAgent("reception")
        
        # Create adoption agent
        self.agents['adoption'] = AdoptionAgent("adoption")
        
        # Create worker agents (caretakers, cleaners, veterinarians)
        for i in range(3):  # Create 3 worker agents
            worker_id = f"worker_{i}"
            self.agents[worker_id] = WorkerAgent(worker_id)
        
        # Create room agents
        for i in range(2):  # Create 2 room agents
            room_id = f"room_{i}"
            self.agents[room_id] = RoomAgent(room_id)
        
        # Create animal assistant agents
        for i in range(3):  # Create 3 animal assistant agents
            animal_id = f"animal_{i}"
            self.agents[animal_id] = AnimalAssistantAgent(animal_id)
        
        # Create applicant agents
        for i in range(2):  # Create 2 applicant agents
            applicant_id = f"applicant_{i}"
            self.agents[applicant_id] = ApplicantAgent(applicant_id)

    async def run_simulation(self):
        print("Starting Multi-Agent System Simulation for Animal Shelter...")
        
        # Start all agents
        tasks = [agent.start() for agent in self.agents.values()]
        
        # Run the simulation for a period of time
        try:
            await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            print("Simulation interrupted by user")
        except Exception as e:
            print(f"Error during simulation: {e}")
        
        print("Simulation completed.")

async def main():
    mas = MultiAgentSystem()
    await mas.run_simulation()

if __name__ == "__main__":
    asyncio.run(main())