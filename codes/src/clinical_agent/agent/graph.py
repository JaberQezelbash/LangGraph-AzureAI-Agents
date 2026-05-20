from langgraph.graph import StateGraph, END
from clinical_agent.agent.state import AgentState
from clinical_agent.agent.model import optional_json_classification, optional_text_generation
from clinical_agent.guardrails.safety import check_input_safety, check_output_safety, detect_emergency
from clinical_agent.tools.mock_ehr import lookup_patient
from clinical_agent.tools.mock_scheduling import find_appointment_slots, create_mock_task


def input_safety_node(state: AgentState) -> AgentState:
    safe, reason = check_input_safety(state.get("user_message", ""))
    return {"input_safe": safe, "input_safety_reason": reason}


def triage_node(state: AgentState) -> AgentState:
    message = state.get("user_message", "")
    lower = message.lower()
    model_result = optional_json_classification(f"Classify this patient message as JSON: {message}")
    intent = model_result.get("intent") if model_result else None
    urgency = model_result.get("urgency") if model_result else None
    sentiment = model_result.get("sentiment") if model_result else None
    specialty = model_result.get("specialty") if model_result else None
    reason = model_result.get("reason") if model_result else "Rule-based triage fallback."

    if detect_emergency(message):
        urgency = "emergency"
        intent = "emergency"
    elif not urgency:
        urgency = "routine"

    if not intent:
        if any(word in lower for word in ["appointment", "schedule", "reschedule", "visit"]):
            intent = "appointment"
        elif any(word in lower for word in ["medication", "lab", "result", "symptom", "pain"]):
            intent = "clinical_question"
        else:
            intent = "general"

    if not specialty:
        if "cardio" in lower or "heart" in lower or "chest" in lower:
            specialty = "cardiology"
        elif "skin" in lower or "rash" in lower:
            specialty = "dermatology"
        elif "diabetes" in lower:
            specialty = "endocrinology"
        else:
            specialty = "primary care"

    if not sentiment:
        sentiment = "concerned" if any(word in lower for word in ["angry", "upset", "frustrated", "worried"]) else "neutral"

    return {"intent": intent, "urgency": urgency, "sentiment": sentiment, "specialty": specialty, "triage_reason": reason}


def ehr_lookup_node(state: AgentState) -> AgentState:
    return {"ehr_context": lookup_patient(state.get("patient_id", "P0000001"))}


def route_decision_node(state: AgentState) -> AgentState:
    if not state.get("input_safe", True):
        return {"route": "human_review_agent", "needs_human": True}
    if state.get("urgency") == "emergency":
        return {"route": "emergency_escalation_agent", "needs_human": True}
    if state.get("intent") == "appointment":
        return {"route": "appointment_agent", "needs_human": False}
    if state.get("intent") == "clinical_question":
        return {"route": "clinical_info_agent", "needs_human": False}
    return {"route": "human_review_agent", "needs_human": True}


def decide_route(state: AgentState) -> str:
    return state.get("route", "human_review_agent")


def appointment_agent(state: AgentState) -> AgentState:
    return {"tool_result": find_appointment_slots(state.get("specialty", "primary care"))}


def clinical_info_agent(state: AgentState) -> AgentState:
    return {"tool_result": create_mock_task(state.get("patient_id", "P0000001"), "clinical_info_agent", "Clinical request reviewed by demo agent.")}


def emergency_escalation_agent(state: AgentState) -> AgentState:
    return {"tool_result": create_mock_task(state.get("patient_id", "P0000001"), "emergency_escalation_agent", "Emergency symptoms detected."), "needs_human": True}


def human_review_agent(state: AgentState) -> AgentState:
    return {"tool_result": create_mock_task(state.get("patient_id", "P0000001"), "human_review_agent", "Message routed to human review."), "needs_human": True}


def response_node(state: AgentState) -> AgentState:
    route = state.get("route", "human_review_agent")
    if route == "emergency_escalation_agent":
        response = "Your message includes symptoms that may be urgent. Please seek emergency medical care immediately or call local emergency services. I am also flagging this message for human review."
    elif route == "appointment_agent":
        slots = state.get("tool_result", {}).get("available_slots", [])
        slot_text = "; ".join([f"{s['date']} at {s['time']} ({s['specialty']})" for s in slots])
        response = f"I found a few demo appointment options: {slot_text}. Please confirm your preferred slot."
    elif route == "clinical_info_agent":
        response = "Thanks for your message. I reviewed the available mock EHR context and flagged your request. This demo provides general information only."
    else:
        response = "Thanks for your message. I am routing this to a human reviewer so the clinic team can follow up safely."

    generated = optional_text_generation(f"Write a brief empathetic patient response for route {route}: {state.get('user_message', '')}")
    if generated:
        response = generated
    return {"draft_response": response, "final_response": response}


def output_safety_node(state: AgentState) -> AgentState:
    safe, reason = check_output_safety(state.get("final_response", ""))
    if not safe:
        return {"output_safe": False, "output_safety_reason": reason, "final_response": "This response was held for human review due to a safety concern.", "needs_human": True}
    return {"output_safe": True, "output_safety_reason": reason}


builder = StateGraph(AgentState)
for name, node in [
    ("input_safety_node", input_safety_node),
    ("triage_node", triage_node),
    ("ehr_lookup_node", ehr_lookup_node),
    ("route_decision_node", route_decision_node),
    ("appointment_agent", appointment_agent),
    ("clinical_info_agent", clinical_info_agent),
    ("emergency_escalation_agent", emergency_escalation_agent),
    ("human_review_agent", human_review_agent),
    ("response_node", response_node),
    ("output_safety_node", output_safety_node),
]:
    builder.add_node(name, node)

builder.set_entry_point("input_safety_node")
builder.add_edge("input_safety_node", "triage_node")
builder.add_edge("triage_node", "ehr_lookup_node")
builder.add_edge("ehr_lookup_node", "route_decision_node")
builder.add_conditional_edges("route_decision_node", decide_route, {
    "appointment_agent": "appointment_agent",
    "clinical_info_agent": "clinical_info_agent",
    "emergency_escalation_agent": "emergency_escalation_agent",
    "human_review_agent": "human_review_agent",
})
builder.add_edge("appointment_agent", "response_node")
builder.add_edge("clinical_info_agent", "response_node")
builder.add_edge("emergency_escalation_agent", "response_node")
builder.add_edge("human_review_agent", "response_node")
builder.add_edge("response_node", "output_safety_node")
builder.add_edge("output_safety_node", END)

graph = builder.compile()
