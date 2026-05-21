# Real Estate Multi-Agent System

A production-grade multi-agent system for real estate analysis based on the GAIA methodology.

## System Overview

This system helps potential homebuyers and renters make informed decisions by analyzing real estate properties based on:

1. **Investment Information**: Planned developments in the area (schools, buildings, services)
2. **Local Opinions**: Reviews of local amenities (restaurants, shops, entertainment)
3. **Price Comparison**: Comparison with similar properties in the area

## Architecture

The system consists of 13 specialized agents working together:

### Core Agents
- **CustomerAgent**: Provides property address and receives final report
- **ReporterAgent**: Coordinates all information and generates final report

### Department Agents (Investment Data)
- **DistrictDepartmentAgent**
- **VoivodeshipDepartmentAgent**
- **CityDepartmentAgent**
- **CountyDepartmentAgent**

### Service Opinion Agents
- **GoogleOpinionsAgent**
- **BookingOpinionsAgent**
- **FacebookOpinionsAgent**
- **TripadvisorOpinionsAgent**

### Price Comparison Agents
- **OLXPricesAgent**
- **OtodomPricesAgent**
- **AllegroPricesAgent**

## How It Works

1. Customer provides property address
2. All agents start their tasks in parallel
3. Each agent retrieves relevant data
4. Reporter agent compiles all information
5. Final report is generated and returned to customer

## Running the System

```bash
python main.py
```

## Requirements

- Python 3.8+
- OpenAI API key (set in .env file)

## License

MIT