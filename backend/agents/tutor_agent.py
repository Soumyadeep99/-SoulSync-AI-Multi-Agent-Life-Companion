class TutorAgent:
    def __init__(self, memory):
        self.memory = memory

    def simple_quiz(self, topic):
        # mock quiz
        return [
            {"q": f"What is a basic concept in {topic}?", "a": "Answer depends on topic."}
        ]

    def handle(self, user_id: str, text: str):
        t = text.lower()

        # Study plan request
        if "study plan" in t or "plan" in t:
            return (
                "Sure! I can help create a study plan.\n"
                "Tell me the subject and how many hours you can study today."
            )

        # Quiz request
        if "quiz" in t or "question" in t:
            quiz = self.simple_quiz("math")
            first_q = quiz[0]["q"]
            return f"Here is a quiz question for you:\n\n❓ {first_q}"

        # Default tutoring response
        return "I'm your tutor! Tell me the subject or topic you want help with."
