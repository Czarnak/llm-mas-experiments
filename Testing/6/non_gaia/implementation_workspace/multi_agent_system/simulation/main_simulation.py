import agentscope
from agentscope.agent import AgentBase
from agentscope.message import Msg
from agents.local_agent import LocalAgent
from agents.business_agent import BusinessAgent
from agents.resident_agent import ResidentAgent
from agents.marketplace_agent import MarketplaceAgent
from agents.matching_engine_agent import MatchingEngineAgent
import numpy as np
import time


def run_simulation():
    print("Starting Multi-Agent System Simulation")
    print("=====================================")
    
    # Initialize agents
    print("1. Initializing agents...")
    
    # Create marketplace agent
    marketplace = MarketplaceAgent(name="Marketplace", agent_id="marketplace_001")
    
    # Create matching engine agent
    matching_engine = MatchingEngineAgent(name="MatchingEngine", agent_id="matching_001", 
                                         min_price=1000, max_price=5000, 
                                         min_size=50, max_size=500)
    
    # Create locals
    local1 = LocalAgent(name="Local1", agent_id="local_001", 
                       location=(52.2297, 21.0122),  # Warsaw
                       price=3000, size=100, business_type="retail")
    
    local2 = LocalAgent(name="Local2", agent_id="local_002", 
                       location=(52.2297, 21.0122),  # Warsaw
                       price=2500, size=150, business_type="restaurant")
    
    local3 = LocalAgent(name="Local3", agent_id="local_003", 
                       location=(52.2297, 21.0122),  # Warsaw
                       price=4000, size=80, business_type="retail")
    
    # Create businesses
    business1 = BusinessAgent(name="Business1", agent_id="business_001", 
                             location=(52.2297, 21.0122),  # Warsaw
                             required_size=120, business_type="retail", max_price=3500)
    
    business2 = BusinessAgent(name="Business2", agent_id="business_002", 
                             location=(52.2297, 21.0122),  # Warsaw
                             required_size=100, business_type="restaurant", max_price=3000)
    
    # Create residents
    resident1 = ResidentAgent(name="Resident1", agent_id="resident_001", 
                             location=(52.2297, 21.0122))
    
    resident2 = ResidentAgent(name="Resident2", agent_id="resident_002", 
                             location=(52.2297, 21.0122))
    
    # Add agents to marketplace
    print("2. Adding agents to marketplace...")
    
    # Add locals to marketplace
    marketplace.add_local(local1)
    marketplace.add_local(local2)
    marketplace.add_local(local3)
    
    # Add businesses to marketplace
    marketplace.add_business(business1)
    marketplace.add_business(business2)
    
    # Add residents to marketplace
    marketplace.add_resident(resident1)
    marketplace.add_resident(resident2)
    
    # Add locals to market
    print("3. Adding locals to market...")
    local1.add_to_market()
    local2.add_to_market()
    local3.add_to_market()
    
    # Place business requirements
    print("4. Placing business requirements...")
    business1.place_requirement()
    business2.place_requirement()
    
    # Place service requests
    print("5. Placing service requests...")
    resident1.place_service_request("home maintenance")
    resident2.place_service_request("cleaning services")
    
    # Find matches
    print("6. Finding matches...")
    
    # Find matches for business1
    matches1 = matching_engine.find_matches(business1, marketplace)
    print(f"Matches for {business1.name}:")
    for local, score in matches1:
        print(f"  - {local.name} (Score: {score:.2f})")
        
    # Find matches for business2
    matches2 = matching_engine.find_matches(business2, marketplace)
    print(f"Matches for {business2.name}:")
    for local, score in matches2:
        print(f"  - {local.name} (Score: {score:.2f})")
    
    # Start auctions
    print("7. Starting auctions...")
    if matches1:
        local_match1 = matches1[0][0]  # Best match
        marketplace.start_auction(business1, local_match1)
        print(f"Auction started between {business1.name} and {local_match1.name}")
        
    if matches2:
        local_match2 = matches2[0][0]  # Best match
        marketplace.start_auction(business2, local_match2)
        print(f"Auction started between {business2.name} and {local_match2.name}")
    
    # Simulate acceptance/rejection
    print("8. Simulating acceptance/rejection...")
    
    # Simulate local accepting business offer
    if matches1:
        print(f"Local {local_match1.name} accepts offer from {business1.name}")
        
    # Simulate local rejecting business offer
    if matches2:
        print(f"Local {local_match2.name} rejects offer from {business2.name}")
        
    # Withdraw offers
    print("9. Withdrawing offers...")
    
    # Withdraw local offers
    local1.withdraw_offer()
    local2.withdraw_offer()
    local3.withdraw_offer()
    
    # Withdraw business requirements
    business1.withdraw_requirement()
    business2.withdraw_requirement()
    
    # Withdraw service requests
    resident1.withdraw_service_request()
    resident2.withdraw_service_request()
    
    print("10. Simulation completed.")
    
    return "Simulation completed successfully"


if __name__ == "__main__":
    result = run_simulation()
    print(result)