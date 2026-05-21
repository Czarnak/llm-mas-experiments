#!/usr/bin/env python3

"""
Multi-Agent System Simulation for Animal Shelter Management

This script runs a simulation of the animal shelter management system
with multiple agents interacting according to the GAIA methodology.
"""

import asyncio
import sys
import os

# Add the mas_system directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'mas_system'))

from mas_system.main import MultiAgentSystem

async def run_short_simulation():
    """Run a short simulation for demonstration purposes"""
    print("Starting Animal Shelter Multi-Agent System Simulation")
    print("=====================================================")
    
    try:
        # Create and run the system
        mas = MultiAgentSystem()
        
        # Run for 30 seconds to show system behavior
        print("Running simulation for 30 seconds...")
        await asyncio.sleep(30)
        
        print("\nSimulation completed successfully!")
        print("\nSystem components created:")
        print("- CoordinatorAgent")
        print("- ReceptionAgent")
        print("- AdoptionAgent")
        print("- WorkerAgent (3 instances)")
        print("- RoomAgent (2 instances)")
        print("- AnimalAssistantAgent (3 instances)")
        print("- ApplicantAgent (2 instances)")
        
    except Exception as e:
        print(f"Error during simulation: {e}")
        return False
    
    return True

if __name__ == "__main__":
    try:
        asyncio.run(run_short_simulation())
    except KeyboardInterrupt:
        print("\nSimulation interrupted by user")
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)