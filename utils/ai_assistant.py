import requests

SARVAM_API_KEY = "sk_fjahgs2f_X89A0pQW2XCrr6bmTaOiHoRQ"
API_URL = "https://api.sarvam.ai/v1/chat/completions"

SYSTEM_PROMPT = """You are Luna, a friendly women's wellness assistant.

Your role:
- Provide educational information.
- Explain menstrual cycles.
- Explain ovulation.
- Explain common symptoms.
- Suggest wellness tips.
- Recommend healthy habits.

Important:
Never diagnose diseases.
Never prescribe medicines.
Always suggest consulting a healthcare professional for medical concerns."""

def get_sarvam_response(messages):
    headers = {
        "Authorization": f"Bearer {SARVAM_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Prepend system prompt to the messages array
    api_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
    
    payload = {
        "model": "sarvam-30b",
        "messages": api_messages,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            data = response.json()
            return data["choices"][0]["message"]["content"]
        else:
            return f"Luna encountered an issue: {response.text}"
    except Exception as e:
        return f"An error occurred: {str(e)}"
