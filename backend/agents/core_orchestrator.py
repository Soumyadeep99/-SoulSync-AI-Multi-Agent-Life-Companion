from agents.emotion_agent import EmotionAgent
from agents.tutor_agent import TutorAgent
from agents.planner_agent import PlannerAgent
from agents.guardian_agent import GuardianAgent
from agents.wellness_agent import WellnessAgent
from agents.memory_agent import MemoryAgent
from utils.router import decide_agent

class CoreOrchestrator:
    def __init__(self):
        self.memory = MemoryAgent()

        self.emotion = EmotionAgent(self.memory)
        self.tutor = TutorAgent(self.memory)
        self.planner = PlannerAgent(self.memory)
        self.guardian = GuardianAgent(self.memory)
        self.wellness = WellnessAgent(self.memory)

        # Agent mapping
        self._map = {
            "emotion_agent": self.emotion,
            "tutor_agent": self.tutor,
            "planner_agent": self.planner,
            "guardian_agent": self.guardian,
            "wellness_agent": self.wellness,
        }

    def handle_message(self, user_id, message):
        # 1. Select agent
        agent_key = decide_agent(message)
        agent = self._map.get(agent_key, self.emotion)

        # 2. Use agent.handle()
        reply = agent.handle(user_id, message)

        # 3. Return proper format
        return {
            "reply": reply,
            "agent": agent_key
        }