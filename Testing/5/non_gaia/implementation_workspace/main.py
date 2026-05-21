import os
from crewai import Agent, Task, Crew
from typing import List, Dict, Any

# Import our custom agents
from agents.resource_requester import ResourceRequesterAgent
from agents.resource_provider import ResourceProviderAgent
from agents.route_planner import RoutePlannerAgent
from agents.traffic_monitor import TrafficMonitorAgent
from agents.notification import NotificationAgent
from agents.emergency_response import EmergencyResponseAgent


class MultiAgentTransportationSystem:
    def __init__(self):
        self.agents = {}
        self.crew = None
        self.setup_agents()
        self.setup_crew()

    def setup_agents(self):
        # Initialize all agents
        self.agents['resource_requester'] = ResourceRequesterAgent().create_agent()
        self.agents['resource_provider'] = ResourceProviderAgent().create_agent()
        self.agents['route_planner'] = RoutePlannerAgent().create_agent()
        self.agents['traffic_monitor'] = TrafficMonitorAgent().create_agent()
        self.agents['notification'] = NotificationAgent().create_agent()
        self.agents['emergency_response'] = EmergencyResponseAgent().create_agent()

    def setup_crew(self):
        # Create a crew to coordinate all agents
        self.crew = Crew(
            agents=list(self.agents.values()),
            tasks=[],  # Tasks will be set during execution
            verbose=True
        )

    def run_simulation(self):
        print("Starting Multi-Agent Transportation & Resource Management System Simulation")
        print("========================================================================")
        
        # Create tasks that will be executed by agents
        tasks = [
            Task(
                description="Request 50 units of medical supplies for Hospital Central with high priority",
                agent=self.agents['resource_requester'],
                expected_output="Resource request details with priority and location"
            ),
            Task(
                description="Find available resources that match the request for medical supplies",
                agent=self.agents['resource_provider'],
                expected_output="List of available medical supplies and providers"
            ),
            Task(
                description="Plan the optimal route from Supply Depot to Hospital Central",
                agent=self.agents['route_planner'],
                expected_output="Optimal delivery route with estimated time"
            ),
            Task(
                description="Monitor traffic conditions and incidents at Main St & 1st Ave",
                agent=self.agents['traffic_monitor'],
                expected_output="Traffic updates and incident reports"
            ),
            Task(
                description="Send notifications about transportation changes",
                agent=self.agents['notification'],
                expected_output="Notification messages sent to relevant parties"
            ),
            Task(
                description="Handle emergency situation and notify law enforcement",
                agent=self.agents['emergency_response'],
                expected_output="Emergency response coordination and law enforcement notification"
            )
        ]
        
        # Execute the tasks
        result = self.crew.kickoff()
        
        print("\nSimulation Complete!")
        print("========================================================================")
        print(result)
        
        return result


def main():
    # Initialize and run the system
    system = MultiAgentTransportationSystem()
    system.run_simulation()


if __name__ == "__main__":
    main()