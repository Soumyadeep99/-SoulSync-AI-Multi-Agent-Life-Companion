import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load your .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ No API Key found. Check your .env file.")
else:
    print(f"✅ Key found: {api_key[:5]}... (hidden)")
    
    try:
        genai.configure(api_key=api_key)
        print("\n🔍 Checking available models for this key...")
        
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"   - {m.name}")
                available_models.append(m.name)
        
        if not available_models:
            print("\n❌ No models found! Your API Key might be invalid or the 'Generative Language API' is not enabled in Google Cloud Console.")
        else:
            print(f"\n✅ SUCCESS! You have access to {len(available_models)} models.")
            print(f"👉 Use this name in your code: '{available_models[0].replace('models/', '')}'")

    except Exception as e:
        print(f"\n❌ Error connecting to Google: {e}")
        