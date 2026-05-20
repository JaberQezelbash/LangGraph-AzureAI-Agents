from pathlib import Path
import sqlite3
from typing import Any

DB_PATH = Path("data/processed/mock_ehr.db")


def lookup_patient(patient_id: str) -> dict[str, Any]:
    if not DB_PATH.exists():
        return {"found": False, "reason": f"Mock EHR database not found at {DB_PATH}"}
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        tables = [row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
        result: dict[str, Any] = {"found": True, "tables": tables, "patient_id": patient_id}
        if "patients" in tables:
            row = conn.execute("SELECT * FROM patients WHERE patient_id = ? LIMIT 1", (patient_id,)).fetchone()
            result["patient"] = dict(row) if row else None
        for table in ["diagnoses", "medications", "lab_results", "outcomes"]:
            if table in tables:
                rows = conn.execute(f"SELECT * FROM {table} WHERE patient_id = ? LIMIT 5", (patient_id,)).fetchall()
                result[table] = [dict(r) for r in rows]
        return result
    finally:
        conn.close()
