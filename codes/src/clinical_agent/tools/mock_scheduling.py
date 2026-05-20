from datetime import datetime, timedelta
from typing import Any


def find_appointment_slots(specialty: str) -> dict[str, Any]:
    today = datetime.utcnow().date()
    slots = []
    for offset in [2, 4, 7]:
        slots.append({"date": str(today + timedelta(days=offset)), "time": "10:00 AM", "specialty": specialty or "primary care", "location": "Demo Clinic"})
    return {"available_slots": slots}


def create_mock_task(patient_id: str, route: str, note: str) -> dict[str, Any]:
    return {"task_created": True, "patient_id": patient_id, "route": route, "note": note}
