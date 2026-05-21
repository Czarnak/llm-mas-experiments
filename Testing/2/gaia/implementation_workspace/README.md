# Multi-Agent System for Cockroach Infestation Detection

This system implements a multi-agent system to detect and respond to cockroach infestations in student dormitories using sensor data.

## System Architecture

The system consists of the following components:

1. **SensorNode** - Physical devices with motion sensors that detect cockroach presence
2. **CentralCoordinator** - Aggregates and processes data from sensor nodes
3. **PatternRecognitionModule** - Analyzes activity patterns to identify high-activity zones
4. **NotificationService** - Sends alerts to relevant stakeholders
5. **BuildingAdministration** - Responds to alerts and manages building operations
6. **PestControlCompany** - Executes treatment for infestations
7. **StudentResident** - Receives notifications about pest issues in their rooms

## Features

- Real-time sensor data collection
- Pattern recognition for high-activity zones
- Automated alerting system
- Multi-stakeholder notifications
- Simulation of the complete system workflow

## How to Run

```bash
python main.py
```

The system will run for 60 seconds demonstrating the complete workflow.