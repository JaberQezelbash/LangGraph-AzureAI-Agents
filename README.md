## AI Agents with LangGraph Orchestration and Azure Deployment




<!-- Optional: add a banner/diagram here -->
<!-- 
<img width="900" alt="banner" src="https://github.com/<YOUR_GITHUB_USERNAME>/<YOUR_REPO_NAME>/blob/main/assets/banner.png">
<img width="800" alt="kan_plot" src="https://github.com/JaberQezelbash/RAG-finetune-Llama-3.1-8B-Instruct/blob/main/assets/model.svg">
-->

<img width="800" alt="kan_plot" src="https://github.com/JaberQezelbash/LangGraph-AzureAI-Agents/blob/main/assets/model.png">


This repository contains an end-to-end AI-agent backend project that receives patient-style messages, classifies the message, routes it through a LangGraph workflow, calls mock clinical tools, applies safety checks, and returns a structured response through a FastAPI API deployed on Azure App Service.

> ⚠️ Disclaimer: This project is for portfolio demonstration only and is not intended for real patient care or clinical decision support.


.
## The product live demo:

After deployment, the API exposes a Swagger/OpenAPI browser UI:

```text
https://app-clinical-langgraph-jaber-5271-afbpbchvfzh5h7ef.eastus2-01.azurewebsites.net/docs
```
A nice user interface is yet to be bulit for it!


## What I Built

This project is a small but complete **cloud-deployed clinical patient-engagement multi-agent API**.

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
    ├── README.md
    ├── technical_details.md
    └── workflow_diagram.mmd


```

The repository is organized in the same portfolio style as my other project repositories: the main source files are under `codes/`, visual and technical explanations are under `assets/`, and the root README provides the high-level story.




## Dataset Design

Original datasets are available here. The project expects dataset categories such as:

* Patient messages or healthcare conversations
* Appointment or scheduling data
* Hospital satisfaction or patient experience data
* EHR-style patient records
* Specialty or symptom labels





## Example API Calls

### Emergency-style request

```powershell
$body = @{
  patient_id = "P0000001"
  user_message = "I have chest pain and shortness of breath."
}
```

Expected emergency routing:

```text
route = emergency_escalation_agent
needs_human = true
urgency = emergency
```



## Author’s Note

This project is a practical, end-to-end demonstration of a cloud-deployed multi-agent clinical AI system. It uses LangGraph to orchestrate multiple agent responsibilities, including message triage, workflow routing, mock EHR/context lookup, safety checks, and response generation, while Azure App Service provides the deployment layer for a live FastAPI-based API demo. I developed a real deployable AI-agent product: from local Python development, to LangGraph workflow design, to Azure deployment, to a public Swagger API interface that can be tested in production-like conditions.
