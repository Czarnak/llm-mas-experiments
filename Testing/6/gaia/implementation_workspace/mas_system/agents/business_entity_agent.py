import spade
from spade.behaviour import OneShotBehaviour, PeriodicBehaviour
from spade.message import Message
from spade.template import Template


class BusinessEntityAgent(spade.agent.Agent):
    def __init__(self, jid, password, business_id):
        super().__init__(jid, password)
        self.business_id = business_id
        self.demands = []
        self.match_criteria = {}
        self.boundary_criteria = {}

    async def setup(self):
        print(f"BusinessEntityAgent {self.jid} starting...")
        
        # Add behaviours for handling messages
        self.add_behaviour(self.SubmitBusinessDemandBehaviour())
        self.add_behaviour(self.RespondToMatchBehaviour())
        self.add_behaviour(self.SetMatchingBoundariesBehaviour())
        self.add_behaviour(self.ListenForMarketplaceMessagesBehaviour())

    class SubmitBusinessDemandBehaviour(OneShotBehaviour):
        async def run(self):
            print(f"BusinessEntityAgent {self.agent.jid} submitting business demand")
            # Send message to Marketplace
            msg = Message(to="marketplace@localhost", 
                         body=f"SubmitBusinessDemand:{self.agent.business_id}:{str(self.agent.match_criteria)}",
                         subject="SubmitBusinessDemand")
            await self.send(msg)
            
            # Store locally
            demand = {
                "business_id": self.agent.business_id,
                "criteria": self.agent.match_criteria
            }
            self.agent.demands.append(demand)
            print(f"Business demand submitted successfully for {self.agent.business_id}")

    class RespondToMatchBehaviour(OneShotBehaviour):
        async def run(self):
            print(f"BusinessEntityAgent {self.agent.jid} responding to match proposal")
            # Send message to Marketplace
            msg = Message(to="marketplace@localhost", 
                         body=f"RespondToMatch:{self.agent.business_id}:ACCEPT",
                         subject="RespondToMatch")
            await self.send(msg)
            
            # In a real implementation, this would receive a match proposal and respond
            # For now, just simulate a response
            print(f"Match response sent for business {self.agent.business_id}")

    class SetMatchingBoundariesBehaviour(OneShotBehaviour):
        async def run(self):
            print(f"BusinessEntityAgent {self.agent.jid} setting matching boundaries")
            # Send message to Marketplace
            msg = Message(to="marketplace@localhost", 
                         body=f"SetMatchingBoundaries:{self.agent.business_id}:{str(self.agent.boundary_criteria)}",
                         subject="SetMatchingBoundaries")
            await self.send(msg)
            
            # Store locally
            print(f"Matching boundaries set for business {self.agent.business_id}")

    class ListenForMarketplaceMessagesBehaviour(PeriodicBehaviour):
        async def run(self):
            # Listen for messages from Marketplace
            template = Template(sender="marketplace@localhost")
            msg = await self.receive(template, timeout=1)
            if msg:
                print(f"BusinessEntityAgent {self.agent.jid} received message: {msg.body}")