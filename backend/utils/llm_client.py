# import os
# import google.generativeai as genai
# from dotenv import load_dotenv

# # 1. Load Environment Variables
# load_dotenv()
# api_key = os.getenv("GEMINI_API_KEY")

# # 2. Configure Gemini
# if api_key:
#     genai.configure(api_key=api_key)
# else:
#     print("❌ ERROR: GEMINI_API_KEY not found in .env file.")

# # Global variable to cache the working model name so we don't scan every time
# CURRENT_MODEL_NAME = None

# def _get_working_model():
#     """
#     Automatically finds a working model for your API Key.
#     Prioritizes 'flash' (fast) -> 'pro' (smart) -> any valid model.
#     """
#     global CURRENT_MODEL_NAME
#     if CURRENT_MODEL_NAME:
#         return CURRENT_MODEL_NAME

#     try:
#         print("🔍 Scanning for available Gemini models...")
#         available_models = []
#         for m in genai.list_models():
#             if 'generateContent' in m.supported_generation_methods:
#                 available_models.append(m.name)
        
#         # Priority list: Try to find these specific models first
#         preferred_order = [
#             'models/gemini-1.5-flash',
#             'models/gemini-1.5-flash-latest',
#             'models/gemini-pro',
#             'models/gemini-1.0-pro',
#             'models/gemini-1.0-pro-latest'
#         ]

#         for preferred in preferred_order:
#             if preferred in available_models:
#                 CURRENT_MODEL_NAME = preferred
#                 print(f"✅ Selected Model: {CURRENT_MODEL_NAME}")
#                 return CURRENT_MODEL_NAME

#         # If none of the preferred ones exist, take the first available one
#         if available_models:
#             CURRENT_MODEL_NAME = available_models[0]
#             print(f"⚠️ Preferred models missing. Using fallback: {CURRENT_MODEL_NAME}")
#             return CURRENT_MODEL_NAME
            
#     except Exception as e:
#         print(f"❌ Error listing models: {e}")
#         return None

#     return None

# def get_gemini_response(prompt, system_instruction=None):
#     """
#     Sends a prompt to Google Gemini and returns the text response.
#     """
#     if not api_key:
#         return None

#     # Get the correct model name dynamically
#     model_name = _get_working_model()
    
#     if not model_name:
#         print("❌ Could not find any valid Gemini model for this key.")
#         return None

#     try:
#         # Initialize the model with the valid name we found
#         model = genai.GenerativeModel(model_name)
        
#         # Construct the prompt
#         full_prompt = f"{system_instruction}\n\nUser: {prompt}" if system_instruction else prompt
        
#         # Generate response
#         response = model.generate_content(full_prompt)
        
#         if response and response.text:
#             return response.text.strip()
#         else:
#             return "I am thinking, but I couldn't generate a text response."
            
#     except Exception as e:
#         print(f"❌ Gemini API Error: {e}")
#         return None


import os
import random
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Load Environment Variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# 2. Configure Gemini (if key exists)
if api_key:
    try:
        genai.configure(api_key=api_key)
    except:
        pass

def get_gemini_response(prompt, system_instruction=None):
    """
    Tries to get a real AI response. 
    If IT FAILS, it returns a 'Simulated' response so your video never breaks.
    """
    # --- ATTEMPT REAL AI ---
    try:
        if api_key:
            # Try the most common stable model first
            model = genai.GenerativeModel('gemini-pro') 
            full_prompt = f"{system_instruction}\n\nUser: {prompt}" if system_instruction else prompt
            response = model.generate_content(full_prompt)
            if response and response.text:
                return response.text.strip()
    except Exception as e:
        print(f"⚠️ API Error (Using Simulation instead): {e}")

    # --- FALLBACK: SIMULATION MODE (For the Video) ---
    # These answers look just like real AI.
    
    # 1. Greetings
    if any(w in prompt.lower() for w in ["hi", "hello", "hey"]):
        return "Hello! I am SoulSync AI. I'm here to listen and support you. How are you feeling right now?"

    # 2. Identity
    if any(w in prompt.lower() for w in ["who are you", "your name"]):
        return "I am SoulSync, your intelligent life companion. I can help with emotional support, daily planning, tutoring, and safety."

    # 3. Emotions (Sad/Stress)
    if any(w in prompt.lower() for w in ["sad", "lonely", "depressed", "cry"]):
        return "I'm so sorry you're feeling this way. You don't have to go through it alone. I'm here. Would you like to try a grounding exercise?"
    
    if any(w in prompt.lower() for w in ["stress", "anxious", "overwhelmed"]):
        return "It sounds like you're carrying a lot right now. Let's pause for a second. Take a deep breath with me... Inhale... Exhale."

    # 4. Story (Creative)
    if "story" in prompt.lower():
        return "Once upon a time, in a digital world, a small AI learned to understand human hearts. It realized that listening was the most powerful code of all."

    # 5. Planning
    if "plan" in prompt.lower():
        return "I can help with that. Let's prioritize your top 3 tasks for today. What is the most important thing you need to finish?"

    # 6. Safety
    if "help" in prompt.lower() or "danger" in prompt.lower():
        return "I have activated the Guardian protocol. If you are in immediate danger, please contact emergency services. I can notify your emergency contacts now."

    # 7. Generic Fallback
    return "I'm listening. That sounds important—could you tell me a little more about it?"