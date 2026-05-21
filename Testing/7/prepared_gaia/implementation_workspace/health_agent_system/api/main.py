from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from system_orchestrator import HealthAgentSystem
import uvicorn

app = FastAPI(title="Health Agent System API")

# Initialize the system
health_system = HealthAgentSystem()


class UserQuery(BaseModel):
    message: str


class ReportResponse(BaseModel):
    id: str
    symptoms: str
    potential_disease: str
    medical_field: str
    timestamp: str
    location: str


class DetailedReportResponse(BaseModel):
    id: str
    location: str
    timestamp: str
    message: str
    medical_data: str


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/query")
def process_query(query: UserQuery):
    try:
        response = health_system.process_user_query(query.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/reports", response_model=List[ReportResponse])
def get_reports():
    try:
        reports = health_system.get_reports()
        return reports
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/reports/{report_id}", response_model=DetailedReportResponse)
def get_detailed_report(report_id: str):
    try:
        report = health_system.get_detailed_report(report_id)
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)