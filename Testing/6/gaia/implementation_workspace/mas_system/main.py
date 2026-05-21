import asyncio
import spade
from agents.property_owner_agent import PropertyOwnerAgent
from agents.business_entity_agent import BusinessEntityAgent
from agents.resident_agent import ResidentAgent
from agents.marketplace_agent import MarketplaceAgent


async def run_system():
    print("Starting Multi-Agent System for City 15-Minute Neighborhoods...")
    
    # Create agents
    marketplace = MarketplaceAgent("marketplace@localhost", "password")
    property_owner = PropertyOwnerAgent("owner@localhost", "password", "PROP001")
    business = BusinessEntityAgent("business@localhost", "password", "BUS001")
    resident = ResidentAgent("resident@localhost", "password", "RES001")
    
    # Start agents
    await marketplace.start()
    await property_owner.start()
    await business.start()
    await resident.start()
    
    print("All agents started successfully")
    
    # Give some time for agents to start
    await asyncio.sleep(1)
    
    # Simulate some interactions by sending messages
    print("\n--- Simulating Property Listing ---")
    # Send message to Marketplace
    msg = spade.message.Message(to="marketplace@localhost", 
                               body="ListProperty:PROP001",
                               subject="ListProperty")
    await property_owner.send(msg)
    
    print("\n--- Simulating Business Demand ---")
    # Send message to Marketplace
    msg = spade.message.Message(to="marketplace@localhost", 
                               body="SubmitBusinessDemand:BUS001:{'price': 1000, 'location': 'center'}",
                               subject="SubmitBusinessDemand")
    await business.send(msg)
    
    print("\n--- Simulating Resident Demand ---")
    # Send message to Marketplace
    msg = spade.message.Message(to="marketplace@localhost", 
                               body="SubmitResidentDemand:RES001:Test service demand",
                               subject="SubmitResidentDemand")
    await resident.send(msg)
    
    # Give some time for message processing
    await asyncio.sleep(2)
    
    # Stop agents
    await marketplace.stop()
    await property_owner.stop()
    await business.stop()
    await resident.stop()
    
    print("\nMulti-Agent System execution completed.")

if __name__ == "__main__":
    asyncio.run(run_system())