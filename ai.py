import os
import json
import re
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("No Gemini API key found in .env. Exiting.")
    exit()

genai.configure(api_key=api_key)

model = genai.GenerativeModel("models/gemini-1.5-flash")

def get_intent_and_entities(user_input):
    """
    Sends user input to Gemini to extract:
    - intent: one of [check_balance, request_leave, cancel_leave, view_history]
    - leave_type: Sick Leave, Annual Leave, Maternity Leave
    - start_date: natural language (e.g., "next Monday")
    - end_date: natural language (e.g., "next Wednesday")
    - num_days: number of leave days
    Returns a dictionary with the above fields.
    """

    prompt = f"""
You are a helpful HR assistant.
Extract the following from the user's message:
- intent: one of [check_balance, request_leave, cancel_leave, view_history]
- leave_type: Sick Leave, Annual Leave, Maternity Leave
- start_date: when the leave starts (just repeat the user's phrase like "next Monday")
- end_date: when the leave ends
- num_days: number of days

Return ONLY a valid JSON object like:
{{
  "intent": "request_leave",
  "leave_type": "Sick Leave",
  "start_date": "next Monday",
  "end_date": "next Wednesday",
  "num_days": 3
}}

User: {user_input}
"""

    try:
        print("Thinking with Gemini...")

        response = model.generate_content(prompt)
        content = response.text.strip()

        print("\nRaw Gemini Response:")
        print(content)

        if content.startswith("```"):
            content = re.sub(r"```(json)?", "", content).strip()
            content = content.replace("```", "").strip()

        print("\nCleaned Response Before Parsing:")
        print(content)

        parsed = json.loads(content)
        print("\nParsed Result:")
        print(parsed)

        return parsed

    except Exception as e:
        print(f"\nERROR: Failed to process Gemini response. Reason: {e}")
        return {
            "intent": "unknown",
            "leave_type": None,
            "start_date": None,
            "end_date": None,
            "num_days": None
        }
