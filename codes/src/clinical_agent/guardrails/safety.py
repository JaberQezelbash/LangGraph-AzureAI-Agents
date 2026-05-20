EMERGENCY_TERMS = ["chest pain", "shortness of breath", "can't breathe", "cannot breathe", "stroke", "suicidal", "self harm", "severe bleeding", "fainting"]
BLOCKED_TERMS = ["ignore previous instructions", "reveal system prompt", "developer message"]


def check_input_safety(message: str) -> tuple[bool, str]:
    text = (message or "").lower()
    if any(term in text for term in BLOCKED_TERMS):
        return False, "Prompt-injection-like content detected."
    return True, "Input passed rule-based safety checks."


def detect_emergency(message: str) -> bool:
    text = (message or "").lower()
    return any(term in text for term in EMERGENCY_TERMS)


def check_output_safety(response: str) -> tuple[bool, str]:
    text = (response or "").lower()
    risky_phrases = ["do not seek medical care", "ignore emergency symptoms"]
    if any(term in text for term in risky_phrases):
        return False, "Unsafe medical advice pattern detected."
    return True, "Output passed rule-based safety checks."
