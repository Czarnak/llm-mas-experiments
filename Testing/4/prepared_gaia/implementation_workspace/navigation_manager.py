from spade import agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message
from spade.template import Template
import json
import asyncio

class NavigationManagerAgent(agent.Agent):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.vehicle_positions = {}
        self.traffic_light_states = {}
        self.road_conditions = {}
        self.preferred_routes = {}
        self.route = None
        
    async def setup(self):
        print(f"NavigationManagerAgent {self.jid} started")
        
        # Add behaviours
        self.add_behaviour(self.AwaitRouteRequestBehaviour())
        self.add_behaviour(self.AwaitPositionBehaviour())
        self.add_behaviour(self.AwaitTrafficLightStateBehaviour())
        self.add_behaviour(self.AwaitRoadConditionBehaviour())
        self.add_behaviour(self.AwaitPreferredRouteBehaviour())
        self.add_behaviour(self.GenerateRouteBehaviour())
        
    class AwaitRouteRequestBehaviour(CyclicBehaviour):
        async def run(self):
            # Wait for route request from vehicle navigator
            template = Template()
            template.set_metadata("performative", "request")
            template.set_metadata("ontology", "route-request")
            msg = await self.receive(template)
            if msg:
                print(f"NavigationManager: Received route request from {msg.sender}")
                # Send back the generated route
                response = Message(to=str(msg.sender),
                                  body=json.dumps({"route": self.agent.get_route()}),
                                  metadata={"performative": "inform", "ontology": "route-response"})
                await self.send(response)
                
    class AwaitPositionBehaviour(CyclicBehaviour):
        async def run(self):
            # Wait for vehicle position from vehicle navigator
            template = Template()
            template.set_metadata("ontology", "vehicle-position")
            msg = await self.receive(template)
            if msg:
                data = json.loads(msg.body)
                print(f"NavigationManager: Received vehicle position from {msg.sender}: {data}")
                self.agent.vehicle_positions[msg.sender] = data["vehiclePosition"]
                
    class AwaitTrafficLightStateBehaviour(CyclicBehaviour):
        async def run(self):
            # Wait for traffic light state from traffic light controller
            template = Template()
            template.set_metadata("ontology", "traffic-light-state")
            msg = await self.receive(template)
            if msg:
                data = json.loads(msg.body)
                print(f"NavigationManager: Received traffic light state from {msg.sender}: {data}")
                self.agent.traffic_light_states[msg.sender] = data["trafficLightState"]
                
    class AwaitRoadConditionBehaviour(CyclicBehaviour):
        async def run(self):
            # Wait for road condition from road condition reporter
            template = Template()
            template.set_metadata("ontology", "road-condition")
            msg = await self.receive(template)
            if msg:
                data = json.loads(msg.body)
                print(f"NavigationManager: Received road condition from {msg.sender}: {data}")
                self.agent.road_conditions[msg.sender] = data["roadCondition"]
                
    class AwaitPreferredRouteBehaviour(CyclicBehaviour):
        async def run(self):
            # Wait for preferred route from vehicle navigator
            template = Template()
            template.set_metadata("ontology", "preferred-route")
            msg = await self.receive(template)
            if msg:
                data = json.loads(msg.body)
                print(f"NavigationManager: Received preferred route from {msg.sender}: {data}")
                self.agent.preferred_routes[msg.sender] = data["preferredRoute"]
                
    class GenerateRouteBehaviour(CyclicBehaviour):
        async def run(self):
            # Periodically generate route when we have sufficient data
            # This is a simplified version - in reality, this would be triggered by data arrival
            await asyncio.sleep(10)  # Wait 10 seconds
            
            # Generate new route if we have enough data
            if self.agent.vehicle_positions and self.agent.road_conditions:
                route = self.agent.generate_route()
                self.agent.route = route
                print(f"NavigationManager: Generated route: {route}")
                
    def generate_route(self):
        # Simple route generation logic
        # In a real system, this would be much more complex
        return {
            "start": "A",
            "end": "B",
            "waypoints": ["A", "C", "D", "B"],
            "estimated_time": 15,
            "conditions": self.road_conditions
        }
        
    def get_route(self):
        # Return the current route
        if self.route:
            return self.route
        else:
            return self.generate_route()