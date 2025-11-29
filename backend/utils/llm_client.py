import os
import google.generativeai as genai
from dotenv import load_dotenv
# 1. Load Environment Variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# 2. Configure Gemini
if api_key:
    genai.configure(api_key=api_key)
else:
    print("❌ ERROR: GEMINI_API_KEY not found in .env file.")

# Global variable to cache the working model name so we don't scan every time
CURRENT_MODEL_NAME = None

def _get_working_model():
    """
    Automatically finds a working model for your API Key.
    Prioritizes 'flash' (fast) -> 'pro' (smart) -> any valid model.
    """
    global CURRENT_MODEL_NAME
    if CURRENT_MODEL_NAME:
        return CURRENT_MODEL_NAME

    try:
        print("🔍 Scanning for available Gemini models...")
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
        
        # Priority list: Try to find these specific models first
        preferred_order = [
            'models/gemini-1.5-flash',
            'models/gemini-1.5-flash-latest',
            'models/gemini-pro',
            'models/gemini-1.0-pro',
            'models/gemini-1.0-pro-latest'
        ]

        for preferred in preferred_order:
            if preferred in available_models:
                CURRENT_MODEL_NAME = preferred
                print(f"✅ Selected Model: {CURRENT_MODEL_NAME}")
                return CURRENT_MODEL_NAME

        # If none of the preferred ones exist, take the first available one
        if available_models:
            CURRENT_MODEL_NAME = available_models[0]
            print(f"⚠️ Preferred models missing. Using fallback: {CURRENT_MODEL_NAME}")
            return CURRENT_MODEL_NAME
            
    except Exception as e:
        print(f"❌ Error listing models: {e}")
        return None

    return None

def get_gemini_response(prompt, system_instruction=None):
    """
    Sends a prompt to Google Gemini and returns the text response.
    """
    if not api_key:
        return None

    # Get the correct model name dynamically
    model_name = _get_working_model()
    
    if not model_name:
        print("❌ Could not find any valid Gemini model for this key.")
        return None

    try:
        # Initialize the model with the valid name we found
        model = genai.GenerativeModel(model_name)
        
        # Construct the prompt
        full_prompt = f"{system_instruction}\n\nUser: {prompt}" if system_instruction else prompt
        
        # Generate response
        response = model.generate_content(full_prompt)
        
        if response and response.text:
            return response.text.strip()
        else:
            return "I am thinking, but I couldn't generate a text response."
            
    except Exception as e:
        print(f"❌ Gemini API Error: {e}")
        return None


