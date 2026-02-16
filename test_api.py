import os
from dotenv import load_dotenv
from groq import Groq

# Load environment
load_dotenv()

api_key = os.environ.get("GROQ_API_KEY")
print(f"API Key from environment: {api_key}")

if not api_key:
    print("ERROR: No API key found")
    exit(1)

try:
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": "Say hello"}
        ],
        max_tokens=100,
    )
    print("✅ API Key is VALID!")
    print(f"Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"❌ API Error: {e}")
