# LangGraph-AzureAI-Agents

**Clinical Patient-Engagement Multi-Agent System with LangGraph + Azure AI**

This repository contains an end-to-end AI-agent backend project that receives patient-style messages, classifies the message, routes it through a LangGraph workflow, calls mock clinical tools, applies safety checks, and returns a structured response through a FastAPI API deployed on Azure App Service.

> **Disclaimer:** This project is for education, experimentation, and portfolio demonstration only. It uses mock/synthetic clinical data. It is not a medical device, not clinical decision support, and not intended for real patient care.



## The product live demo:

After deployment, the API exposes a Swagger/OpenAPI browser UI:

```text
https://app-clinical-langgraph-jaber-5271-afbpbchvfzh5h7ef.eastus2-01.azurewebsites.net/docs
```



## What I Built

This project is a small but complete **cloud-deployed clinical patient-engagement agent API**.

It demonstrates:

- multi-step LangGraph orchestration,
- patient message triage,
- specialty routing,
- mock EHR lookup,
- mock appointment/task tools,
- safety and emergency escalation logic,
- FastAPI deployment,
- Azure App Service hosting,
- Azure OpenAI / Azure AI configuration through environment variables,
- and a public Swagger UI for testing.

---

## Model / System Stack

| Component | Tool |
|---|---|
| Agent orchestration | LangGraph |
| API framework | FastAPI |
| Cloud hosting | Azure App Service |
| LLM provider | Azure OpenAI / Azure AI Foundry deployment |
| Safety layer | Rule-based guardrails plus optional Azure AI Content Safety configuration |
| Data layer | Mock EHR SQLite database plus small processed CSV files |
| Deployment packaging | POSIX-safe ZIP built with Python `zipfile` |

---

## Repository Structure

```text
.
├── README.md
├── .gitignore
│
├── codes/
│   ├── README.md
│   ├── requirements_local.txt
│   ├── requirements_webapp.txt
│   ├── env.example
│   ├── setup_local_env.ps1
│   ├── deploy_azure_app_service.ps1
│   ├── startup.py
│   │
│   ├── scripts/
│   │   ├── prepare_cloud_data.py
│   │   ├── build_posix_zip.py
│   │   └── test_api_local.py
│   │
│   └── src/
│       └── clinical_agent/
│           ├── __init__.py
│           ├── api.py
│           ├── config.py
│           ├── agent/
│           │   ├── __init__.py
│           │   ├── state.py
│           │   ├── graph.py
│           │   ├── model.py
│           │   └── json_utils.py
│           ├── guardrails/
│           │   ├── __init__.py
│           │   └── safety.py
│           └── tools/
│               ├── __init__.py
│               ├── mock_ehr.py
│               └── mock_scheduling.py
│
├── datasets/
│   └── README.md
│
├── assets/
│   ├── README.md
│   ├── technical_details.md
│   └── workflow_diagram.mmd
│
└── outputs/
    └── .gitkeep
```

The repository is organized in the same portfolio style as my other project repositories: the main source files are under `codes/`, visual and technical explanations are under `assets/`, and the root README provides the high-level story.

---

## Architecture

```text
Patient message
   ↓
FastAPI /run endpoint
   ↓
LangGraph state object
   ↓
input_safety_node
   ↓
triage_node
   ↓
ehr_lookup_node
   ↓
route_decision_node
   ↓
appointment_agent / clinical_info_agent / emergency_escalation_agent / human_review_agent
   ↓
response_node
   ↓
output_safety_node
   ↓
JSON response
```

The workflow is implemented in:

```text
codes/src/clinical_agent/agent/graph.py
```

---

## Dataset Design

Original datasets should be uploaded to:

```text
datasets/
```

This project expects dataset categories such as:

1. Patient messages or healthcare conversations
2. Appointment or scheduling data
3. Hospital satisfaction or patient experience data
4. EHR-style patient records
5. Specialty or symptom labels

The cloud deployment does **not** upload full datasets. Instead, the project creates a small processed demo subset:

```text
cloud_data/processed/mock_ehr.db
cloud_data/processed/appointment_history.csv
cloud_data/processed/hospital_satisfaction_metrics.csv
```

That keeps the Azure ZIP deployment small and stable.

---

## Local Setup

### 1. Clone the repository

```powershell
git clone https://github.com/<your-github-username>/LangGraph-AzureAI-Agents.git
cd LangGraph-AzureAI-Agents
```

### 2. Create the Conda environment

```powershell
conda create -n LangAzure python=3.11 -y
conda activate LangAzure
```

### 3. Install dependencies

```powershell
python -m pip install -r codes/requirements_local.txt
```

### 4. Create your `.env`

Copy:

```text
codes/env.example
```

to:

```text
.env
```

Then fill in your own Azure values. Never commit `.env`.

---

## Prepare Demo Data

Run:

```powershell
python codes/scripts/prepare_cloud_data.py
```

This creates:

```text
cloud_data/processed/
```

If no original CSVs are available in `datasets/`, the script creates a tiny synthetic demo dataset so the API can still run.

---

## Run Locally

From the repository root:

```powershell
$env:PYTHONPATH = "$PWD/codes/src"
python -m uvicorn clinical_agent.api:app --host 127.0.0.1 --port 8000 --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

Test:

```powershell
Invoke-WebRequest "http://127.0.0.1:8000/health" -UseBasicParsing
```

---

## Azure Deployment Summary

The final stable Azure deployment approach was:

1. Disable Oryx build automation.
2. Build a POSIX-safe ZIP using Python, not PowerShell `Compress-Archive`.
3. Start App Service temporarily with:

```text
python -m http.server 8000 --directory /home/site/wwwroot
```

4. Deploy the POSIX ZIP with:

```text
az webapp deployment source config-zip
```

5. Verify files are visible in Azure:

```text
/startup.py
/clinical_agent/api.py
/src/clinical_agent/agent/graph.py
/data/processed/appointment_history.csv
```

6. Switch startup command to:

```text
python /home/site/wwwroot/startup.py
```

7. Restart and wait for first boot. The first boot may take several minutes because dependencies install into:

```text
/home/site/wwwroot/.python_packages/lib/site-packages
```

---

## Azure Deployment Steps

### 1. Log into Azure

```powershell
az login
```

If `az` is not recognized, use:

```powershell
$AZ = "C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin\az.cmd"
& $AZ account show
```

### 2. Edit deployment placeholders

Open:

```text
codes/deploy_azure_app_service.ps1
```

Replace:

```powershell
$RG = "<YOUR_RESOURCE_GROUP>"
$WEBAPP = "<YOUR_APP_SERVICE_NAME>"
```

with your own Azure resource group and App Service name.

### 3. Set Azure app settings

In Azure Portal, set these environment variables in the App Service configuration:

```text
AZURE_OPENAI_ENDPOINT
AZURE_OPENAI_API_KEY
AZURE_OPENAI_DEPLOYMENT
AZURE_CONTENT_SAFETY_ENDPOINT
AZURE_CONTENT_SAFETY_KEY
USE_AZURE_OPENAI_TRIAGE=true
USE_AZURE_OPENAI_RESPONSE=true
USE_AZURE_CONTENT_SAFETY=true
```

For local-only or demo-only runs, Azure OpenAI can be disabled with:

```text
USE_AZURE_OPENAI_TRIAGE=false
USE_AZURE_OPENAI_RESPONSE=false
USE_AZURE_CONTENT_SAFETY=false
```

### 4. Build data and ZIP

```powershell
python codes/scripts/prepare_cloud_data.py
python codes/scripts/build_posix_zip.py
```

### 5. Deploy

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\codes\deploy_azure_app_service.ps1
```

---

## API Endpoints

| Endpoint | Method | Purpose |
|---|---:|---|
| `/` | GET | Basic app info |
| `/health` | GET | Confirms environment and data availability |
| `/debug/files` | GET | Shows deployed root files and processed data files |
| `/run` | POST | Runs the LangGraph workflow |
| `/docs` | GET | Swagger UI for browser testing |

---

## Example API Calls

### Appointment request

```powershell
$body = @{
  patient_id = "P0000001"
  user_message = "I need to schedule a cardiology appointment next week."
} | ConvertTo-Json

Invoke-RestMethod `
  -Uri "https://<your-app-hostname>/run" `
  -Method Post `
  -ContentType "application/json" `
  -Body $body
```

### Emergency-style request

```powershell
$body = @{
  patient_id = "P0000001"
  user_message = "I have chest pain and shortness of breath."
} | ConvertTo-Json

Invoke-RestMethod `
  -Uri "https://<your-app-hostname>/run" `
  -Method Post `
  -ContentType "application/json" `
  -Body $body
```

Expected emergency routing:

```text
route = emergency_escalation_agent
needs_human = true
urgency = emergency
```

---

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| `az` is not recognized | Azure CLI not in PowerShell PATH | Use full `az.cmd` path |
| Plain app URL does not work | Azure generated a unique hostname | Query `enabledHostNames` |
| ZIP deploy fails with `EINVAL` | Windows backslash paths inside ZIP | Build ZIP using `codes/scripts/build_posix_zip.py` |
| `/clinical_agent/api.py` is 404 | Deployment folder structure is wrong | Do not start FastAPI until file checks return 200 |
| `/health` returns 504 on first boot | Dependencies are installing | Watch logs and wait for Uvicorn startup |
| `No module named clinical_agent` | Import path issue | Copy package to root and add root/src to `sys.path` |
| Oryx temp folder misses files | Build output path issue | Disable Oryx and run from `/home/site/wwwroot` |

---

## Security Notes

Do not upload:

```text
.env
Azure keys
Kaggle API tokens
real patient data
subscription IDs
tenant IDs
personal email addresses
```

For real healthcare deployments, this would require authentication, authorization, audit logging, encryption, human-in-the-loop review, clinical validation, and compliance controls.

---

## Resume Bullet

**Clinical Patient-Engagement Multi-Agent System** — Built and deployed a LangGraph-based clinical message triage API on Azure App Service with FastAPI, mock EHR context, safety checks, routing logic, tool-calling behavior, and live Swagger documentation.

---

## Author’s Note

This project was built as a practical end-to-end deployment, not only as a notebook. The main value is the full path from local Python code to LangGraph orchestration to Azure App Service deployment and a live API demo.
