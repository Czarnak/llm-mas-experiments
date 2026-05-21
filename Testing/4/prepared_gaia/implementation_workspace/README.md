# Multi-Agent System for Urban Traffic Management

This is a production-grade multi-agent system designed to dynamically support privileged vehicles (ambulances, fire trucks) in urban traffic conditions, minimizing disruptions and improving road safety.

## System Overview

The system consists of multiple autonomous agents that communicate to:
- Track vehicle positions in real-time
- Monitor road conditions and traffic events
- Optimize routes for privileged vehicles
- Coordinate traffic light signals
- Alert drivers about approaching privileged vehicles

## Agents

1. **VehicleNavigator** - Tracks vehicle position and generates preferred routes
2. **TrafficLightController** - Controls traffic lights based on vehicle priority
3. **RoadConditionReporter** - Reports random events on the road
4. **DriverAlertingSystem** - Manages alerts for drivers about traffic conditions
5. **NavigationManager** - Coordinates all information to generate optimal routes

## Features

- Real-time position tracking
- Dynamic route optimization
- Traffic light coordination
- Event monitoring and reporting
- Driver alert systems

## Running the System

```bash
python main.py
```
