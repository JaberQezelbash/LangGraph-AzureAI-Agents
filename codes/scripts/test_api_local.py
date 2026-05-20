import json
import sys
import requests

BASE_URL = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000"
print("Testing", BASE_URL)
print(requests.get(f"{BASE_URL}/health", timeout=20).json())

payload = {"patient_id": "P0000001", "user_message": "I need to schedule a cardiology appointment next week."}
print(json.dumps(requests.post(f"{BASE_URL}/run", json=payload, timeout=60).json(), indent=2))

payload = {"patient_id": "P0000001", "user_message": "I have chest pain and shortness of breath."}
print(json.dumps(requests.post(f"{BASE_URL}/run", json=payload, timeout=60).json(), indent=2))
