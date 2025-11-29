class WellnessAgent:
    def __init__(self, memory):
        self.memory = memory

    def handle(self, user_id: str, text: str):
        t = text.lower()

        # Detect breathing requests
        if "breath" in t or "breathe" in t or "breathing" in t:
            return (
                "🧘 Let's try a quick breathing exercise:\n"
                "• Inhale for 4 seconds\n"
                "• Hold for 4 seconds\n"
                "• Exhale for 6 seconds\n"
                "Repeat this for 1 minute. I'm here with you."
            )

        # Sleep-related advice
        if "sleep" in t or "insomnia" in t or "tired" in t:
            return (
                "😴 Here's a simple sleep routine:\n"
                "• No screens 30 minutes before bed\n"
                "• Dim the lights\n"
                "• Take slow deep breaths\n"
                "• Try light stretching or warm water on face\n"
                "Let me know if you'd like a guided relaxation."
            )

        # Default fallback
        return (
            "I can help with wellness routines like breathing, grounding exercises, "
            "small walks, and relaxation. Just tell me what you need."
        )
