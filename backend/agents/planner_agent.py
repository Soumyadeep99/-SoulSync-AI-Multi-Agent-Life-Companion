from datetime import datetime, timedelta

class PlannerAgent:
    def __init__(self, memory):
        self.memory = memory

    def handle(self, user_id: str, text: str):
        t = text.lower()

        # Basic planner behavior
        if "plan my day" in t or "plan" in t:
            now = datetime.utcnow()

            schedule = [
                {"time": (now + timedelta(hours=1)).isoformat(), "task": "Focused study (1h)"},
                {"time": (now + timedelta(hours=2)).isoformat(), "task": "Break (20m)"},
                {"time": (now + timedelta(hours=3)).isoformat(), "task": "Practice problems (1h)"}
            ]

            # Save schedule in memory for later reference
            self.memory.add_note(
                user_id,
                {
                    "type": "schedule",
                    "schedule": schedule,
                    "at": now.isoformat()
                }
            )

            # Return clean text message (required by orchestrator)
            return (
                "Here's a quick plan for your day:\n"
                f"🕒 {schedule[0]['time']}: {schedule[0]['task']}\n"
                f"🕒 {schedule[1]['time']}: {schedule[1]['task']}\n"
                f"🕒 {schedule[2]['time']}: {schedule[2]['task']}\n"
                "\nLet me know if you want to adjust any task."
            )

        # Default response
        return "I can help you organize your tasks. Try saying 'Plan my day'."
