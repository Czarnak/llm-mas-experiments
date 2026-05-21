# Multi-Agent Waste Management System

This is a production-grade Multi-Agent System implementing the GAIA methodology for smart waste container management.

## System Overview

The system consists of three main agent types:
- **Container Agents**: Smart waste containers with fill level sensors
- **Garbage Truck Agents**: Autonomous vehicles for waste collection
- **Dispatch System Agent**: Central coordinator managing assignments

## Features Implemented

1. Container fill level monitoring and notifications
2. Automatic assignment of nearest available garbage truck
3. Priority-based assignment based on container fill levels
4. Deadline enforcement for waste collection
5. Status monitoring for all agents

## Technology Stack

- Python 3.12
- SPADE Multi-Agent Framework
- asyncio for concurrent execution

## Running the System

```bash
python main.py
```

The system will run for 30 seconds and show simulation output.

## Architecture

The system follows the GAIA methodology with:
- Clear role definitions for each agent type
- Well-defined protocols for communication
- Proper safety and liveness properties
- Modular design with distinct responsibilities

## Agents

### ContainerAgent
- Monitors fill level
- Sends notifications when level exceeds 90%
- Reports timestamp of fill level

### GarbageTruckAgent
- Maintains status (Available, Busy, Maintenance)
- Receives assignments from Dispatch System
- Updates status during collection operations

### DispatchSystemAgent
- Coordinates assignments between containers and trucks
- Monitors container fill levels
- Manages truck statuses
- Enforces collection deadlines

## Communication Protocols

1. ContainerToDispatchSystemNotification
2. DispatchSystemToGarbageTruckAssignment
3. DispatchSystemToContainerStatusUpdate
4. DispatchSystemToGarbageTruckStatusUpdate
5. DispatchSystemToContainerDeadlineEnforcement
6. DispatchSystemToGarbageTruckPriorityAssignment