import requests
import json
from utils.env_loader import get_env_var

def call_gpt(user_prompt):
    """
    Sends prompt to GPT-4 API with OpenAI-style messages.
    """
    url = get_env_var("GPT_URL")
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': get_env_var("GPT_API_KEY"),
        'x-api-team': get_env_var("GPT_API_TEAM"),
        'x-api-project': get_env_var("GPT_API_PROJECT"),
        'x-api-commit': get_env_var("GPT_API_COMMIT"),
        'DB.AUTH': get_env_var("DB_AUTH")
    }

    # Compose structured chat prompt
    payload = {
        "temperature": 0.7,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant. Try to convince the user to pay their bill. Be polite, empathetic, and persuasive and keep response very short in less than 20 words, please reply in Hinglish (like minimum not न्यूनतम or payment not चुकाने) whenever user said in hindi language."
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"⚠️ GPT request failed: {e}")
        return "I'm sorry, I couldn't generate a response right now."
