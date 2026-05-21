# Crisis Transport Management Multi-Agent System

This is a production-grade Multi-Agent System designed for crisis transport management based on the GAIA methodology.

## System Overview

The system manages transportation and resource allocation during crisis situations like floods. It consists of three main agents:

1. **ResourceCoordinatorAgent** - Handles resource requests, offers, and matching
2. **TransportPlannerAgent** - Manages transport route planning and updates
3. **NotificationAgent** - Sends emergency notifications

## Components

### Data Models
- ResourceRequest: Formal request for specific resources
- ResourceOffer: Offer to provide specific resources
- ResourceMatch: Result of matching requests with offers
- TransportRoute: Planned or actual transport route
- RouteUpdate: Update to existing transport route
- RoadBlockageReport: Report of road blockages
- EmergencyNotification: Notification to users about emergencies
- SpecializedNotification: Specialized notification to emergency services

### Agents
- ResourceCoordinatorAgent
- TransportPlannerAgent
- NotificationAgent

## Implementation

This system is built using Python with the AgentScope framework for multi-agent communication.

## Running the System

To run a simulation of the system:

```bash
python main.py
```
