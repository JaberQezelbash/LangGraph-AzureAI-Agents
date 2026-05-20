from typing import Any, TypedDict


class AgentState(TypedDict, total=False):
    run_id: str
    patient_id: str
    user_message: str
    input_safe: bool
    input_safety_reason: str
    intent: str
    urgency: str
    sentiment: str
    specialty: str
    triage_reason: str
    ehr_context: dict[str, Any]
    route: str
    tool_result: dict[str, Any]
    needs_human: bool
    draft_response: str
    final_response: str
    output_safe: bool
    output_safety_reason: str
