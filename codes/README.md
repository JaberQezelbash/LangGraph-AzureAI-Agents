# codes/

This folder contains the reproducible code for the LangGraph + Azure AI clinical agent project.

## Main files

```text
requirements_local.txt          Local development dependencies
requirements_webapp.txt         Minimal cloud runtime dependencies
env.example                     Safe environment-variable template
setup_local_env.ps1             Beginner local setup commands
deploy_azure_app_service.ps1    Azure App Service deployment script
startup.py                      Azure runtime startup file
scripts/prepare_cloud_data.py   Creates small cloud demo data
scripts/build_posix_zip.py      Builds Linux-safe deployment ZIP
scripts/test_api_local.py       Tests local or deployed API endpoints
src/clinical_agent/             FastAPI + LangGraph source code
```

## Recommended workflow

```powershell
conda activate LangAzure
python codes/scripts/prepare_cloud_data.py
python codes/scripts/build_posix_zip.py
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\codes\deploy_azure_app_service.ps1
```

Edit all placeholders in the deployment script before using it.
