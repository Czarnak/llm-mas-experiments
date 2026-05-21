import asyncio
import logging
from collector_agent import CollectorAgent
from communicator_agent import CommunicatorAgent
from container_agent import ContainerAgent

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def run_system():
    print("Starting Garbage Collection Multi-Agent System")
    
    # Create agents
    # Collector agents
    collector1 = CollectorAgent("collector1@localhost", "password1", (10, 20))
    collector2 = CollectorAgent("collector2@localhost", "password2", (30, 40))
    collector3 = CollectorAgent("collector3@localhost", "password3", (50, 60))
    
    # Communicator agent
    communicator = CommunicatorAgent("communicator@localhost", "password")
    
    # Container agents
    container1 = ContainerAgent("container1@localhost", "password1", (15, 25))
    container2 = ContainerAgent("container2@localhost", "password2", (35, 45))
    container3 = ContainerAgent("container3@localhost", "password3", (55, 65))
    
    # Start agents
    await collector1.start()
    await collector2.start()
    await collector3.start()
    await communicator.start()
    await container1.start()
    await container2.start()
    await container3.start()
    
    print("All agents started successfully")
    
    # Let the system run for a while to demonstrate the coordination
    await asyncio.sleep(60)
    
    # Stop agents
    await collector1.stop()
    await collector2.stop()
    await collector3.stop()
    await communicator.stop()
    await container1.stop()
    await container2.stop()
    await container3.stop()
    
    print("System shutdown complete")

if __name__ == "__main__":
    try:
        asyncio.run(run_system())
    except KeyboardInterrupt:
        print("System interrupted by user")
    except Exception as e:
        print(f"System error: {e}")