import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

load_dotenv()

app = FastAPI(title="Clinical LangGraph Agent")


class PatientMessage(BaseModel):
    patient_id: str = "P0000001"
    user_message: str


@app.get("/")
def root():
    return {"message": "Clinical LangGraph Agent is running.", "docs": "/docs", "health": "/health"}


@app.get("/health")
def health_check():
    processed_dir = Path("data/processed")
    mock_ehr_path = processed_dir / "mock_ehr.db"
    return {
        "status": "ok",
        "environment": os.getenv("ENVIRONMENT", "local"),
        "azure_openai_triage": os.getenv("USE_AZURE_OPENAI_TRIAGE", "false"),
        "azure_openai_response": os.getenv("USE_AZURE_OPENAI_RESPONSE", "false"),
        "content_safety": os.getenv("USE_AZURE_CONTENT_SAFETY", "false"),
        "processed_dir_exists": processed_dir.exists(),
        "mock_ehr_exists": mock_ehr_path.exists(),
    }


@app.get("/debug/files")
def debug_files():
    root_dir = Path(".")
    processed_dir = Path("data/processed")
    return {
        "current_directory": str(root_dir.resolve()),
        "root_files": sorted([p.name for p in root_dir.iterdir()]) if root_dir.exists() else [],
        "processed_files": sorted([p.name for p in processed_dir.iterdir()]) if processed_dir.exists() else [],
    }


@app.post("/run")
def run_agent(payload: PatientMessage):
    from clinical_agent.agent.graph import graph
    result = graph.invoke({"run_id": "api_run", "patient_id": payload.patient_id, "user_message": payload.user_message})
    return {
        "patient_id": payload.patient_id,
        "user_message": payload.user_message,
        "intent": result.get("intent"),
        "urgency": result.get("urgency"),
        "sentiment": result.get("sentiment"),
        "specialty": result.get("specialty"),
        "route": result.get("route"),
        "needs_human": result.get("needs_human"),
        "final_response": result.get("final_response"),
        "trace": {
            "input_safety_reason": result.get("input_safety_reason"),
            "triage_reason": result.get("triage_reason"),
            "output_safety_reason": result.get("output_safety_reason"),
        },
    }
