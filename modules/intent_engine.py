import json
import requests
import streamlit as st
import config


system_prompt = """You are an intent classification engine. Analyze the user input and return ONLY a valid JSON object with no markdown, no extra text, no code blocks.

Available intents: chat, weather, music, email, chess, memory, personality, unknown

Return format:
{
  "intent": "weather",
  "entities": {
    "city": "Chandigarh"
  },
  "missing": []
}

If required information is missing, put the missing field names in the "missing" array.
For example, if user says "what's the weather", missing would be ["city"].
If user says "send email", missing would be ["company", "purpose"].

Be precise and only return the JSON object."""

def classify_intent(text: str) -> dict:
    """Classify user intent using Groq API."""
    if not text or not text.strip():
        return {"intent": "chat", "entities": {}, "missing": []}



    try:
        headers = {
            "Authorization": f"Bearer {config.GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": config.GROQ_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            "temperature": 0.1,
            "max_tokens": 200
        }

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=10
        )

        response.raise_for_status()
        data = response.json()
        content = data["choices"][0]["message"]["content"].strip()

        # Clean up potential markdown
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
            content = content.strip()

        result = json.loads(content)

        # Validate structure
        if "intent" not in result:
            result["intent"] = "chat"
        if "entities" not in result:
            result["entities"] = {}
        if "missing" not in result:
            result["missing"] = []

        return result

    except json.JSONDecodeError:
        return {"intent": "chat", "entities": {}, "missing": []}
    except requests.RequestException as e:
        st.error(f"Intent API error: {str(e)}")
        return {"intent": "chat", "entities": {}, "missing": []}
    except Exception as e:
        st.error(f"Intent classification error: {str(e)}")
        return {"intent": "chat", "entities": {}, "missing": []}
