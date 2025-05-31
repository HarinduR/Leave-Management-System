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
    - start_date: natural language 
    - end_date: natural language 
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
        print("\nThinking with Gemini...")

        response = model.generate_content(prompt)
        content = response.text.strip()

        if content.startswith("```"):
            content = re.sub(r"```(json)?", "", content).strip()
            content = content.replace("```", "").strip()

        parsed = json.loads(content)
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

def generate_natural_response(name, intent, leave_type=None, num_days=None, start=None, end=None, balance=None, status=None):

    prompt = f"""
You are an HR assistant bot. Based on the info below, respond to the user in a friendly, natural tone.

User name: {name}
Intent: {intent}
Leave Type: {leave_type}
Start Date: {start}
End Date: {end}
Number of Days: {num_days}
Leave Balance: {balance}
Status (e.g., Approved, Cancelled): {status}

Examples of response styles:
- "Hi Sarah, your 2-day sick leave from June 3 to June 4 has been recorded."
- "You have 3 annual leaves left. Make the most of them!"
- "Sorry, your leave request can’t be processed due to insufficient balance."

Now write the response for this situation:
"""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return "Sorry, I couldn't generate a friendly response at the moment."
