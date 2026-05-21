# Health Multi-Agent System

A production-grade multi-agent system for health data analysis and symptom reporting.

## Features

- **Symptom Reporting**: Intuitive interface for users to report symptoms
- **Health Data Analysis**: Real-time analysis of health data
- **Health Authority Support**: Provides insights to health institutions and researchers
- **User Recommendations**: Personalized health recommendations for users
- **LLM Integration**: Powered by large language models for intelligent processing
- **Scalable Architecture**: Multi-agent system designed for high scalability
- **Security**: Data protection compliant with regulations
- **Availability**: 24/7 accessible system
- **Usability**: Simple and intuitive user interface

## Architecture

The system is built using a multi-agent architecture with the following core agents:

1. **Symptom Reporter Agent**: Collects and analyzes user-reported symptoms
2. **Health Data Analyzer Agent**: Processes and analyzes health data in real-time
3. **Health Authority Support Agent**: Provides structured data and insights to health authorities
4. **User Recommendation Agent**: Generates personalized health recommendations

## Technologies

- Python 3.12+
- CrewAI (Multi-agent framework)
- FastAPI (Web framework)
- OpenAI API (LLM integration)
- SQLite (Database)
- Pydantic (Data validation)

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Create a `.env` file in the root directory with the following content:

```
OPENAI_API_KEY=your_openai_api_key_here
SECRET_KEY=your_secret_key_here
```

## Running the System

```bash
python main.py
```

The system will start a FastAPI server on port 8000 with the following endpoints:

- `GET /health` - Health check endpoint
- `POST /report-symptoms` - Report symptoms
- `GET /analyze-health-data` - Analyze health data
- `GET /authority-report` - Generate authority report
- `GET /research-insights` - Generate research insights
- `GET /user-recommendations/{user_id}` - Get user recommendations

## API Usage Examples

### Report Symptoms

```bash
POST /report-symptoms
{
  "user_id": "user_001",
  "symptoms": ["fever", "headache"],
  "severity": "moderate",
  "duration": "days",
  "additional_notes": "User reports feeling unwell"
}
```

### Analyze Health Data

```bash
GET /analyze-health-data
```

### Get Authority Report

```bash
GET /authority-report
```

## Security

The system implements:
- Data encryption
- Secure authentication
- Privacy compliance

## Scalability

The system is designed to handle:
- High concurrent user loads
- Large-scale data processing
- Distributed computing capabilities

## Contributing

Contributions are welcome. Please follow the existing code style and add appropriate tests.

## License

MIT License