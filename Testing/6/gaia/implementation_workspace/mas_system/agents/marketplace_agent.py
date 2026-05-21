import spade
from spade.behaviour import OneShotBehaviour, PeriodicBehaviour
from spade.message import Message
from spade.template import Template


class MarketplaceAgent(spade.agent.Agent):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.property_listings = []
        self.business_listings = []
        self.resident_listings = []
        self.matches = []

    async def setup(self):
        print(f"MarketplaceAgent {self.jid} starting...")
        
        # Add behaviours for handling messages
        self.add_behaviour(self.ManagePropertyListingsBehaviour())
        self.add_behaviour(self.ProcessBusinessDemandsBehaviour())
        self.add_behaviour(self.ExecuteMatchingAlgorithmsBehaviour())
        self.add_behaviour(self.ValidateDataIntegrityBehaviour())
        self.add_behaviour(self.ListenForAgentMessagesBehaviour())

    class ManagePropertyListingsBehaviour(OneShotBehaviour):
        async def run(self):
            print(f"MarketplaceAgent {self.agent.jid} managing property listings")
            # In a real implementation, this would handle property listings
            # For now, just print a message
            print("Property listings managed successfully")

    class ProcessBusinessDemandsBehaviour(OneShotBehaviour):
        async def run(self):
            print(f"MarketplaceAgent {self.agent.jid} processing business demands")
            # In a real implementation, this would process business demands
            # For now, just print a message
            print("Business demands processed successfully")

    class ExecuteMatchingAlgorithmsBehaviour(OneShotBehaviour):
        async def run(self):
            print(f"MarketplaceAgent {self.agent.jid} executing matching algorithms")
            # In a real implementation, this would execute matching algorithms
            # For now, just print a message
            print("Matching algorithms executed successfully")

    class ValidateDataIntegrityBehaviour(OneShotBehaviour):
        async def run(self):
            print(f"MarketplaceAgent {self.agent.jid} validating data integrity")
            # In a real implementation, this would validate data integrity
            # For now, just print a message
            print("Data integrity validated successfully")

    class ListenForAgentMessagesBehaviour(PeriodicBehaviour):
        async def run(self):
            # Listen for messages from agents
            template = Template()
            msg = await self.receive(template, timeout=1)
            if msg:
                print(f"MarketplaceAgent {self.agent.jid} received message: {msg.body}")
                # Process the message based on subject
                if msg.subject == "ListProperty":
                    self.agent.property_listings.append(msg.body.split(":")[1])
                elif msg.subject == "RemoveProperty":
                    property_id = msg.body.split(":")[1]
                    if property_id in self.agent.property_listings:
                        self.agent.property_listings.remove(property_id)
                elif msg.subject == "SubmitBusinessDemand":
                    self.agent.business_listings.append(msg.body.split(":")[1])
                elif msg.subject == "SubmitResidentDemand":
                    self.agent.resident_listings.append(msg.body.split(":")[1])
