import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from system_coordinator import HealthSystemCoordinator
from agents.symptom_reporter import SymptomReport
from config.settings import settings

app = FastAPI(title="Health Multi-Agent System", version="1.0.0")
coordinator = HealthSystemCoordinator()


class HealthReportRequest(BaseModel):
    user_id: str
    symptoms: List[str]
    severity: str  # mild, moderate, severe
    duration: str  # hours, days, weeks
    additional_notes: str = ""


class HealthReportResponse(BaseModel):
    status: str
    report: Dict[str, Any]
    recommendations: List[Dict[str, Any]]
    advice: str


@ app.post("/report-symptoms", response_model=HealthReportResponse)
async def report_symptoms(request: HealthReportRequest):
    try:
        report = SymptomReport(
            symptoms=request.symptoms,
            severity=request.severity,
            duration=request.duration,
            additional_notes=request.additional_notes
        )
        
        result = coordinator.process_symptom_report(report, request.user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@ app.get("/analyze-health-data")
async def analyze_health_data():
    try:
        result = coordinator.analyze_health_data()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@ app.get("/authority-report")
async def get_authority_report():
    try:
        result = coordinator.generate_authority_report()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@ app.get("/research-insights")
async def get_research_insights():
    try:
        result = coordinator.generate_research_insights()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@ app.get("/user-recommendations/{user_id}")
async def get_user_recommendations(user_id: str):
    try:
        result = coordinator.get_user_recommendations(user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@ app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Health Multi-Agent System"}


if __name__ == "__main__":
    print("Starting Health Multi-Agent System...")
    print("System initialized with the following agents:")
    print("- Symptom Reporter Agent")
    print("- Health Data Analyzer Agent")
    print("- Health Authority Support Agent")
    print("- User Recommendation Agent")
    
    # Run a quick simulation
    print("\nRunning simulation...")
    
    # Simulate a user reporting symptoms
    test_report = SymptomReport(
        symptoms=["fever", "headache"],
        severity="moderate",
        duration="days",
        additional_notes="User reports feeling unwell"
    )
    
    result = coordinator.process_symptom_report(test_report, "user_001")
    print(f"\nSymptom report processed: {result['status']}")
    print(f"Recommendations: {len(result['recommendations'])} items")
    
    # Analyze health data
    analysis = coordinator.analyze_health_data()
    print(f"\nHealth data analyzed: {analysis['analysis']['total_reports']} reports processed")
    
    # Generate authority report
    authority_report = coordinator.generate_authority_report()
    print(f"\nAuthority report generated: {authority_report['authority_report'].report_type}")
    
    print("\nSimulation completed successfully!")
    
    # Start the FastAPI server
    uvicorn.run(app, host="0.0.0.0", port=8000)