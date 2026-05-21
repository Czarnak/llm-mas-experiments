# Crisis Transportation Management Multi-Agent System

This is a production-grade Multi-Agent System designed for crisis transportation management, implementing the GAIA methodology as specified in the requirements.

## System Overview

The system manages transportation logistics during crisis situations (like floods) by coordinating multiple agents to:
- Report resource needs
- Match available resources with needs
- Plan and optimize delivery routes
- Notify relevant parties about changes

## Agents

The system consists of the following agent types:

1. **PersonInNeedAgent** - Reports resource needs
2. **HelperAgent** - Offers to provide resources
3. **DataHandlerAgent** - Manages database of requests and available materials
4. **NotifierAgent** - Sends notifications about changes and alerts
5. **RoutePlannerAgent** - Plans delivery routes
6. **TruckDriverAgent** - Delivers resources
7. **ServicesAgent** - Receives special notifications for emergency services

## Architecture

The system uses the SPADe framework for multi-agent communication and coordination.

## Getting Started

1. Install dependencies: `pip install -r requirements.txt`
2. Run the system: `python run_system.py`

## Implementation Details

This implementation follows the GAIA methodology with defined roles, protocols, and interactions between agents.