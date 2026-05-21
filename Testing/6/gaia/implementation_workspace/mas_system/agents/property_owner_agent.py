import spade
from spade.behaviour import OneShotBehaviour, PeriodicBehaviour
from spade.message import Message
from spade.template import Template


class PropertyOwnerAgent(spade.agent.Agent):
    def __init__(self, jid, password, property_id):
        super().__init__(jid, password)
        self.property_id = property_id
        self.property_listings = []
        self.property_offers = []

    async def setup(self):
        print(f"PropertyOwnerAgent {self.jid} starting...")
        
        # Add behaviours for handling messages
        self.add_behaviour(self.ListPropertyBehaviour())
        self.add_behaviour(self.RemovePropertyBehaviour())
        self.add_behaviour(self.WithdrawPropertyOfferBehaviour())
        self.add_behaviour(self.ListenForMarketplaceMessagesBehaviour())

    class ListPropertyBehaviour(OneShotBehaviour):
        async def run(self):
            print(f"PropertyOwnerAgent {self.agent.jid} listing property {self.agent.property_id}")
            # Send message to Marketplace
            msg = Message(to="marketplace@localhost", 
                         body=f"ListProperty:{self.agent.property_id}",
                         subject="ListProperty")
            await self.send(msg)
            
            # Store locally
            self.agent.property_listings.append(self.agent.property_id)
            self.agent.property_offers.append(self.agent.property_id)
            print(f"Property {self.agent.property_id} listed successfully")

    class RemovePropertyBehaviour(OneShotBehaviour):
        async def run(self):
            print(f"PropertyOwnerAgent {self.agent.jid} removing property {self.agent.property_id}")
            # Send message to Marketplace
            msg = Message(to="marketplace@localhost", 
                         body=f"RemoveProperty:{self.agent.property_id}",
                         subject="RemoveProperty")
            await self.send(msg)
            
            # Store locally
            if self.agent.property_id in self.agent.property_listings:
                self.agent.property_listings.remove(self.agent.property_id)
            if self.agent.property_id in self.agent.property_offers:
                self.agent.property_offers.remove(self.agent.property_id)
            print(f"Property {self.agent.property_id} removed successfully")

    class WithdrawPropertyOfferBehaviour(OneShotBehaviour):
        async def run(self):
            print(f"PropertyOwnerAgent {self.agent.jid} withdrawing offer for property {self.agent.property_id}")
            # Send message to Marketplace
            msg = Message(to="marketplace@localhost", 
                         body=f"WithdrawPropertyOffer:{self.agent.property_id}",
                         subject="WithdrawPropertyOffer")
            await self.send(msg)
            
            # Store locally
            if self.agent.property_id in self.agent.property_offers:
                self.agent.property_offers.remove(self.agent.property_id)
            print(f"Offer for property {self.agent.property_id} withdrawn successfully")

    class ListenForMarketplaceMessagesBehaviour(PeriodicBehaviour):
        async def run(self):
            # Listen for messages from Marketplace
            template = Template(sender="marketplace@localhost")
            msg = await self.receive(template, timeout=1)
            if msg:
                print(f"PropertyOwnerAgent {self.agent.jid} received message: {msg.body}")