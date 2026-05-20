from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATASETS = ROOT / "datasets"
OUT = ROOT / "cloud_data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)


def find_csv(name_hint: str) -> Path | None:
    for path in DATASETS.glob("*.csv"):
        if name_hint.lower() in path.name.lower():
            return path
    return None


def write_demo_appointment_csv(path: Path) -> None:
    pd.DataFrame([
        {"patient_id": "P0000001", "specialty": "cardiology", "appointment_date": "2026-06-01", "status": "completed"},
        {"patient_id": "P0000002", "specialty": "primary care", "appointment_date": "2026-06-02", "status": "scheduled"},
    ]).to_csv(path, index=False)


def write_demo_satisfaction_csv(path: Path) -> None:
    pd.DataFrame([
        {"facility_name": "Demo Clinic", "rating": 4.7, "metric": "patient_experience"},
        {"facility_name": "Demo Hospital", "rating": 4.2, "metric": "timeliness"},
    ]).to_csv(path, index=False)


def create_mock_ehr_db(path: Path) -> None:
    if path.exists():
        path.unlink()
    conn = sqlite3.connect(path)
    try:
        conn.execute("CREATE TABLE patients (patient_id TEXT PRIMARY KEY, age INTEGER, sex TEXT, primary_condition TEXT, preferred_specialty TEXT)")
        conn.execute("CREATE TABLE diagnoses (patient_id TEXT, diagnosis TEXT, diagnosis_date TEXT)")
        conn.execute("CREATE TABLE medications (patient_id TEXT, medication TEXT, status TEXT)")
        conn.execute("CREATE TABLE lab_results (patient_id TEXT, lab_name TEXT, lab_value TEXT, result_date TEXT)")
        conn.execute("CREATE TABLE outcomes (patient_id TEXT, outcome_name TEXT, outcome_value TEXT)")
        conn.execute("INSERT INTO patients VALUES (?, ?, ?, ?, ?)", ("P0000001", 54, "F", "hypertension", "cardiology"))
        conn.execute("INSERT INTO diagnoses VALUES (?, ?, ?)", ("P0000001", "hypertension", "2025-09-01"))
        conn.execute("INSERT INTO medications VALUES (?, ?, ?)", ("P0000001", "demo medication", "active"))
        conn.execute("INSERT INTO lab_results VALUES (?, ?, ?, ?)", ("P0000001", "A1C", "6.1", "2026-01-05"))
        conn.execute("INSERT INTO outcomes VALUES (?, ?, ?)", ("P0000001", "last_visit", "completed"))
        conn.commit()
    finally:
        conn.close()


def main() -> None:
    appointment_out = OUT / "appointment_history.csv"
    satisfaction_out = OUT / "hospital_satisfaction_metrics.csv"
    db_out = OUT / "mock_ehr.db"
    appointment_source = find_csv("appointment")
    satisfaction_source = find_csv("satisfaction") or find_csv("hospital")
    if appointment_source:
        pd.read_csv(appointment_source).head(300).to_csv(appointment_out, index=False)
    else:
        write_demo_appointment_csv(appointment_out)
    if satisfaction_source:
        pd.read_csv(satisfaction_source).head(300).to_csv(satisfaction_out, index=False)
    else:
        write_demo_satisfaction_csv(satisfaction_out)
    create_mock_ehr_db(db_out)
    print("Created cloud demo data:")
    for path in OUT.glob("*"):
        print(f" - {path} ({path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
