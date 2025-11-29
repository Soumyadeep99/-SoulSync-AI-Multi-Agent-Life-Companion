def decide_agent(text: str) -> str:
    """Basic intent heuristics to choose an agent."""
    t = text.lower()
    
    # Guardian / Safety
    if any(w in t for w in ["safe", "danger", "help me", "sos", "emergency", "scared", "threat"]):
        return "guardian_agent"
    
    # Tutor / Education
    if any(w in t for w in ["study", "exam", "question", "solve", "teach", "learn", "math", "physics"]):
        return "tutor_agent"
    
    # Planner / Productivity
    if any(w in t for w in ["plan", "schedule", "todo", "remind", "task", "agenda", "calendar"]):
        return "planner_agent"
    
    # Wellness / Health
    if any(w in t for w in ["sleep", "health", "burnout", "wellness", "breath", "exercise", "tired"]):
        return "wellness_agent"
    
    # Default to Emotion Agent for chat, greetings, and feelings
    return "emotion_agent"