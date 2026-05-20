from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import shutil

ROOT = Path(__file__).resolve().parents[2]
DEPLOY = ROOT / "deploy_app"
ZIP_PATH = ROOT / "deploy_app_posix.zip"
CODES = ROOT / "codes"
CLOUD = ROOT / "cloud_data" / "processed"

if DEPLOY.exists():
    shutil.rmtree(DEPLOY)
if ZIP_PATH.exists():
    ZIP_PATH.unlink()

(DEPLOY / "data" / "processed").mkdir(parents=True, exist_ok=True)
shutil.copy2(CODES / "startup.py", DEPLOY / "startup.py")
shutil.copytree(CODES / "src", DEPLOY / "src")
shutil.copytree(CODES / "src" / "clinical_agent", DEPLOY / "clinical_agent")
shutil.copy2(CODES / "requirements_webapp.txt", DEPLOY / "requirements.txt")

if not CLOUD.exists():
    raise SystemExit("cloud_data/processed does not exist. Run: python codes/scripts/prepare_cloud_data.py")
for item in CLOUD.iterdir():
    if item.is_file():
        shutil.copy2(item, DEPLOY / "data" / "processed" / item.name)

for bad_dir in DEPLOY.rglob("__pycache__"):
    shutil.rmtree(bad_dir, ignore_errors=True)
for pyc in DEPLOY.rglob("*.pyc"):
    pyc.unlink(missing_ok=True)

with ZipFile(ZIP_PATH, "w", ZIP_DEFLATED) as z:
    for path in DEPLOY.rglob("*"):
        if path.is_file():
            z.write(path, path.relative_to(DEPLOY).as_posix())

with ZipFile(ZIP_PATH) as z:
    names = z.namelist()
bad_backslashes = [n for n in names if "\\" in n]
required = ["startup.py", "clinical_agent/api.py", "src/clinical_agent/api.py", "src/clinical_agent/agent/graph.py", "data/processed/mock_ehr.db", "data/processed/appointment_history.csv", "data/processed/hospital_satisfaction_metrics.csv", "requirements.txt"]
missing = [item for item in required if item not in names]
print("ZIP file:", ZIP_PATH)
print("File count:", len(names))
print("Backslash paths:", bad_backslashes)
print("Has clinical_agent/api.py:", "clinical_agent/api.py" in names)
print("Has data/processed/mock_ehr.db:", "data/processed/mock_ehr.db" in names)
if bad_backslashes:
    raise SystemExit("BAD ZIP: contains Windows backslash paths.")
if missing:
    raise SystemExit(f"BAD ZIP: missing {missing}")
print("POSIX ZIP looks good.")
