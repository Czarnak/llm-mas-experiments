# Multi-Agent Transportation & Resource Management System

## Overview
This is a production-grade multi-agent system designed to manage resource requests, supply-demand matching, and transportation coordination with dynamic route optimization.

## System Components

### Agent Types
1. **ResourceRequesterAgent** - Requests specific resources
2. **ResourceProviderAgent** - Offers available resources
3. **RoutePlannerAgent** - Plans optimal transportation routes
4. **TrafficMonitorAgent** - Monitors traffic conditions and incidents
5. **NotificationAgent** - Sends notifications to relevant parties
6. **EmergencyResponseAgent** - Handles emergency situations and special notifications

### Key Functionalities
- Resource request/offering matching
- Route planning and optimization
- Dynamic route adjustment for accidents/traffic
- Communication of road blockages and threats
- Notification systems for transportation changes
- Special notifications for law enforcement

## Running the System

```bash
python main.py
```

## Architecture
The system uses CrewAI framework to coordinate agents through a central coordinator that manages communication and task distribution.
