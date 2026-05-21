from mas_system.agents.premise_for_rent_agent import PremiseForRentAgent
from mas_system.agents.future_tenant_agent import FutureTenantAgent
from mas_system.agents.citizen_agent import CitizenAgent
from mas_system.agents.auction_hub_agent import AuctionHubAgent
from mas_system.utils.logger import log_system_event


def run_simulation():
    """
    Run a simulation of the Multi-Agent System without SPADE agents
    """
    print("Starting Multi-Agent System Simulation (Simplified)...")
    
    # Create agents
    auction_hub = AuctionHubAgent("auction_hub@localhost", "password", "AuctionHub")
    premise_agent = PremiseForRentAgent("premise@localhost", "password", "PremiseForRent")
    tenant_agent = FutureTenantAgent("tenant@localhost", "password", "FutureTenant")
    citizen_agent = CitizenAgent("citizen@localhost", "password", "Citizen")
    
    # Register premises
    auction_hub.register_premise(
        premise_id="PREMISE_001",
        location="Downtown",
        price=2000.0,
        size=50.0,
        business_type="cafe"
    )
    
    # Register tenants
    auction_hub.register_tenant(
        tenant_id="TENANT_001",
        business_type="cafe",
        preferred_location="Downtown",
        max_price=2500.0
    )
    
    # Report service demand
    citizen_agent.set_citizen_details("CITIZEN_001", "Downtown")
    demand = citizen_agent.report_service_demand("coffee_shop", "high")
    
    # Process service demand through auction hub
    auction_hub.process_service_demand(
        citizen_id="CITIZEN_001",
        service_type="coffee_shop",
        location="Downtown",
        priority="high"
    )
    
    # Create premise offer
    premise_agent.set_premise_details(
        premise_id="PREMISE_001",
        location="Downtown",
        price=2000.0,
        size=50.0,
        business_type="cafe"
    )
    
    premise_offer = premise_agent.create_premise_offer()
    
    # Send premise offer to auction hub (simulated)
    log_system_event("Sending Premise Offer", f"Sending offer for {premise_offer.get('premise_id', 'unknown')}")
    
    # Create tenant offer
    tenant_agent.set_tenant_details(
        tenant_id="TENANT_001",
        business_type="cafe",
        preferred_location="Downtown",
        max_price=2500.0
    )
    
    tenant_offer = tenant_agent.create_tenant_offer("PREMISE_001")
    
    # Send tenant offer to auction hub (simulated)
    log_system_event("Sending Tenant Offer", f"Sending offer for {tenant_offer.get('tenant_id', 'unknown')} to {tenant_offer.get('premise_id', 'unknown')}")
    
    # Process matching
    log_system_event("Processing Matches")
    matches = auction_hub.match_premises_and_tenants()
    
    # Display results
    print("\n=== MATCHING RESULTS ===")
    for match_id, match_info in matches.items():
        print(f"Match ID: {match_id}")
        print(f"  Premise: {match_info['premise_id']}")
        print(f"  Tenant: {match_info['tenant_id']}")
        print(f"  Match Score: {match_info['match_score']}")
        print()
    
    # Cancel premise offer
    log_system_event("Canceling Premise Offer")
    auction_hub.cancel_premise_offer("PREMISE_001")
    
    # Withdraw service demand
    log_system_event("Withdrawing Service Demand")
    citizen_agent.withdraw_demand()
    
    print("Simulation completed.")

if __name__ == "__main__":
    run_simulation()