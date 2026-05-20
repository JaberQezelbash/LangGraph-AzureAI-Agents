# Technical Details

This document provides deeper implementation notes for the LangGraph + Azure AI clinical agent project.

---

## System Goal

The project implements a small clinical message-routing backend. It demonstrates multi-step agent orchestration, triage, mock tool calling, mock EHR lookup, guardrails, structured output, and cloud deployment.

The project is a portfolio and learning demo, not a real clinical product.

---

## LangGraph Design

The graph is implemented in:

```text
codes/src/clinical_agent/agent/graph.py
```

The state object is implemented in:

```text
codes/src/clinical_agent/agent/state.py
```

Main nodes:

```text
input_safety_node
triage_node
ehr_lookup_node
route_decision_node
appointment_agent
clinical_info_agent
emergency_escalation_agent
human_review_agent
response_node
output_safety_node
```

The routing node uses conditional edges to decide which specialized agent should run next.

---

## Azure App Service Startup Flow

Final working flow:

1. Disable Oryx build automation.
2. Package source code and processed demo data into a POSIX ZIP.
3. Temporarily run:

```text
python -m http.server 8000 --directory /home/site/wwwroot
```

4. Deploy ZIP with:

```text
az webapp deployment source config-zip
```

5. Verify deployed files through the temporary HTTP server.
6. Set startup command:

```text
python /home/site/wwwroot/startup.py
```

7. Restart and wait for dependency installation.

---

## Deployment Lesson

PowerShell `Compress-Archive` can create Windows-style path separators in ZIP files. Linux App Service expects POSIX-style paths.

Bad path:

```text
clinical_agent\agent\graph.py
```

Good path:

```text
clinical_agent/agent/graph.py
```

The fix is implemented in:

```text
codes/scripts/build_posix_zip.py
```

using:

```python
arcname = path.relative_to(root).as_posix()
```

---

## Safety and Guardrails

Implemented in:

```text
codes/src/clinical_agent/guardrails/safety.py
```

The demo includes prompt-injection checks, emergency symptom detection, output safety checks, and human-review routing.

---

## Azure OpenAI Integration

Azure OpenAI calls are optional and controlled by:

```text
USE_AZURE_OPENAI_TRIAGE
USE_AZURE_OPENAI_RESPONSE
AZURE_OPENAI_ENDPOINT
AZURE_OPENAI_API_KEY
AZURE_OPENAI_DEPLOYMENT
```

If Azure OpenAI is not configured, the workflow falls back to deterministic rule-based triage and response generation.

---

## Limitations

This demo does not include user authentication, audit logging, real EHR integration, clinical validation, real HIPAA compliance controls, or real patient data.

---

## Future Improvements

1. Add API-key authentication to protect Azure quota.
2. Add Application Insights tracing.
3. Add structured evaluation datasets.
4. Add human-in-the-loop approval states.
5. Add Azure AI Search for RAG over policy documents.
6. Add a simple frontend.
7. Add GitHub Actions deployment automation.
