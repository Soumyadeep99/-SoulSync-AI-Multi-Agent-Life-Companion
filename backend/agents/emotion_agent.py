# from utils.llm_client import get_gemini_response

# class EmotionAgent:
#     def __init__(self, memory):
#         self.memory = memory

#     def handle(self, user_id, message):
#         print(f"🤖 AI Request for: {message}")

#         # 1. Define the AI Persona
#         system_prompt = (
#             "You are SoulSync AI, a warm, compassionate, and helpful life companion. "
#             "Your goal is to provide emotional support and helpful advice. "
#             "Keep your answers concise (2-3 sentences). Do not give medical advice."
#         )

#         # 2. Call Gemini (Using the correct function name)
#         ai_reply = get_gemini_response(message, system_instruction=system_prompt)

#         # 3. Return AI reply if successful
#         if ai_reply:
#             return ai_reply
        
#         # 4. Fallback if Gemini fails
#         return "I am having trouble connecting to my AI brain. Please check your API Key."


from utils.llm_client import get_gemini_response

class EmotionAgent:
    def __init__(self, memory):
        self.memory = memory

    def handle(self, user_id, message):
        print(f"🤖 Processing: {message}")

        # Define the AI Persona
        system_prompt = (
            "You are SoulSync AI, a warm and helpful companion. "
            "Answer briefly and kindly."
        )

        # Call the Magic Client (Will use Real AI or Simulation automatically)
        reply = get_gemini_response(message, system_instruction=system_prompt)
        
        return reply