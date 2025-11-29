class GuardianAgent:
    def __init__(self, memory):
        self.memory = memory

    def handle(self, user_id: str, text: str):
        t = text.lower()

        # Emergency trigger keywords
        if "sos" in t or "help me" in t or "danger" in t:
            # Safely read memory (avoid crashes for new users)
            user_data = self.memory.get_user(user_id)
            if not user_data:
                contact = "Emergency contact not set"
            else:
                profile = user_data.get("profile", {})
                contact = profile.get("emergency_contact", "Emergency contact not set")

            # This is a mock response — real alert logic goes later
            return (
                f"🚨 Emergency Protocol Activated.\n"
                f"Notifying: {contact} (demo mode).\n"
                f"If you are in immediate danger, please call your local emergency number right now."
            )

        # Default help message
        return "I can help during emergencies. Say 'SOS' if you need urgent assistance."
