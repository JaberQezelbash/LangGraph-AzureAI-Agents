import os
import sys
import subprocess
from pathlib import Path

print("===== startup.py: raw /home/site/wwwroot deployment =====", flush=True)

ROOT = Path("/home/site/wwwroot").resolve()
os.chdir(ROOT)

PKG_DIR = ROOT / ".python_packages" / "lib" / "site-packages"
PKG_DIR.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(PKG_DIR))
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

print(f"ROOT={ROOT}", flush=True)
print(f"Current directory={Path.cwd()}", flush=True)
print(f"Root files={[p.name for p in ROOT.iterdir()]}", flush=True)

processed_dir = ROOT / "data" / "processed"
mock_ehr = processed_dir / "mock_ehr.db"
print(f"processed_dir_exists={processed_dir.exists()}", flush=True)
print(f"mock_ehr_exists={mock_ehr.exists()}", flush=True)

REQ = ROOT / "requirements.txt"


def ensure_dependencies() -> None:
    try:
        import fastapi  # noqa: F401
        import uvicorn  # noqa: F401
        import langgraph  # noqa: F401
        import pandas  # noqa: F401
        print("Core dependencies already import OK.", flush=True)
        return
    except Exception as exc:
        print(f"Dependencies missing, installing now: {exc}", flush=True)

    if not REQ.exists():
        raise FileNotFoundError(f"requirements.txt not found at {REQ}")

    subprocess.check_call([
        sys.executable,
        "-m",
        "pip",
        "install",
        "--no-cache-dir",
        "--upgrade",
        "-r",
        str(REQ),
        "--target",
        str(PKG_DIR),
    ])
    sys.path.insert(0, str(PKG_DIR))


ensure_dependencies()

import fastapi  # noqa: F401
print("FastAPI import OK", flush=True)

import uvicorn
print("Uvicorn import OK", flush=True)

from clinical_agent.api import app
print("clinical_agent.api import OK", flush=True)

port = int(os.environ.get("PORT", "8000"))
print(f"Starting uvicorn on port {port}", flush=True)

uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
