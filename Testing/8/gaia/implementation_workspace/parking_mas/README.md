# Parking Management Multi-Agent System

This is a production-grade Multi-Agent System for managing parking spaces based on the GAIA methodology.

## System Overview

The system consists of multiple agents that collaborate to help drivers find and reserve parking spaces efficiently:

- **User Agent**: Represents individual users who interact with the system
- **Reservation System Agent**: Central system managing reservations and availability
- **Parking Lot Agent**: Represents physical parking lots with available spaces
- **Payment Processor Agent**: Handles payment processing for reservations

## Architecture

The system follows the GAIA methodology with defined roles, interactions, and services.

## Implementation Details

The implementation uses Python with the SPADE framework for multi-agent communication.

## Running the System

To run the simulation:

```bash
python main.py
```

## Key Features

1. Real-time parking availability checking
2. Reservation system with space blocking
3. Reservation cancellation and modification
4. Payment processing
5. Multi-agent communication

## Components

- `models/`: Data models for ParkingLot, Reservation, User, Payment
- `agents/`: Agent implementations
- `utils/`: Utility functions and logging
- `main.py`: Main application entry point

## Requirements

- Python 3.7+
- SPADE framework

## License

MIT License