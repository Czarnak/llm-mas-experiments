import spade
from spade.behaviour import OneShotBehaviour, PeriodicBehaviour
from spade.message import Message
from spade.template import Template


class ResidentAgent(spade.agent.Agent):
    def __init__(self, jid, password, resident_id):
        super().__init__(jid, password)
        self.resident_id = resident_id
        self.service_demands = []

    async def setup(self):
        print(f"ResidentAgent {self.jid} starting...")
        
        # Add behaviours for handling messages
        self.add_behaviour(self.SubmitResidentDemandBehaviour())
        self.add_behaviour(self.WithdrawResidentDemandBehaviour())
        self.add_behaviour(self.ListenForMarketplaceMessagesBehaviour())

    class SubmitResidentDemandBehaviour(OneShotBehaviour):
        async def run(self):
            print(f"ResidentAgent {self.agent.jid} submitting service demand")
            # Send message to Marketplace
            msg = Message(to="marketplace@localhost", 
                         body=f"SubmitResidentDemand:{self.agent.resident_id}:Test service demand",
                         subject="SubmitResidentDemand")
            await self.send(msg)
            
            # Store locally
            demand = {
                "resident_id": self.agent.resident_id,
                "service_demand": "Test service demand"
            }
            self.agent.service_demands.append(demand)
            print(f"Service demand submitted successfully for {self.agent.resident_id}")

    class WithdrawResidentDemandBehaviour(OneShotBehaviour):
        async def run(self):
            print(f"ResidentAgent {self.agent.jid} withdrawing service demand")
            # Send message to Marketplace
            msg = Message(to="marketplace@localhost", 
                         body=f"WithdrawResidentDemand:{self.agent.resident_id}:Test service demand",
                         subject="WithdrawResidentDemand")
            await self.send(msg)
            
            # Store locally
            if self.agent.service_demands:
                self.agent.service_demands.pop()
            print(f"Service demand withdrawn successfully for {self.agent.resident_id}")

    class ListenForMarketplaceMessagesBehaviour(PeriodicBehaviour):
        async def run(self):
            # Listen for messages from Marketplace
            template = Template(sender="marketplace@localhost")
            msg = await self.receive(template, timeout=1)
            if msg:
                print(f"ResidentAgent {self.agent.jid} received message: {msg.body}")
