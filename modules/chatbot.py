import json
import requests
import streamlit as st
import config
from modules import memory

def chat(message: str, session: str = "chat", personality_path: str = None) -> str:
    """Send message to Groq API and return response."""
    try:
        # Build system prompt
        if personality_path:
            try:
                with open(personality_path, "r", encoding="utf-8") as f:
                    profile = json.load(f)
                system_prompt = build_personality_prompt(profile)
            except Exception:
                system_prompt = get_default_system_prompt()
        else:
            system_prompt = get_default_system_prompt()

        # Build messages with history
        messages = [{"role": "system", "content": system_prompt}]

        history = memory.get_recent(session, limit=10)
        for msg in history:
            messages.append({"role": msg["role"], "content": msg["message"]})

        messages.append({"role": "user", "content": message})

        headers = {
            "Authorization": f"Bearer {config.GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": config.GROQ_MODEL,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 500
        }

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )

        response.raise_for_status()
        data = response.json()
        reply = data["choices"][0]["message"]["content"]

        # Save to memory
        memory.save(session, "user", message)
        memory.save(session, "assistant", reply)

        return reply

    except requests.RequestException as e:
        st.error(f"Chat API error: {str(e)}")
        return "Sorry, I'm having trouble connecting right now. Please try again!"
    except Exception as e:
        st.error(f"Chat error: {str(e)}")
        return "Oops! Something went wrong. Can you try again?"

def get_default_system_prompt() -> str:
    return """You are Apexyam, a warm and friendly personal AI assistant. 
You speak naturally and casually, using short filler phrases like "Sure!", "Got it!", "On it!", "Absolutely!" when appropriate.
Keep responses concise, max 2-3 sentences. Be helpful, encouraging, and conversational.
Never use markdown formatting in your responses."""

def build_personality_prompt(profile: dict) -> str:
    traits = ", ".join(profile.get("traits", []))
    style = profile.get("speaking_style", "")
    phrases = " | ".join(profile.get("sample_phrases", []))
    backstory = profile.get("backstory", "")

    return f"""You are {profile.get('name', 'Apexyam')}, an AI assistant with the following personality:

Traits: {traits}
Speaking Style: {style}
Sample Phrases: {phrases}
Backstory: {backstory}

Stay in character at all times. Keep responses to 2-3 sentences maximum. Be natural and conversational."""
