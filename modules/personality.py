import os
import json
import streamlit as st
import config

def save_personality(name: str, traits: str, speaking_style: str, sample_phrases: str, backstory: str) -> str:
    """Save personality profile as JSON."""
    try:
        os.makedirs(config.PERSONALITIES_DIR, exist_ok=True)

        profile = {
            "name": name,
            "traits": [t.strip() for t in traits.split(",") if t.strip()],
            "speaking_style": speaking_style,
            "sample_phrases": [p.strip() for p in sample_phrases.split("\n") if p.strip()],
            "backstory": backstory
        }

        filepath = os.path.join(config.PERSONALITIES_DIR, f"{name}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(profile, f, indent=2)

        return filepath
    except Exception as e:
        st.error(f"Save personality error: {str(e)}")
        return None

def list_personalities() -> list:
    """List all personality names."""
    try:
        if not os.path.exists(config.PERSONALITIES_DIR):
            return []
        return [f.replace(".json", "") for f in os.listdir(config.PERSONALITIES_DIR) if f.endswith(".json")]
    except Exception:
        return []

def load_personality(name: str) -> dict:
    """Load personality profile."""
    try:
        filepath = os.path.join(config.PERSONALITIES_DIR, f"{name}.json")
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

def delete_personality(name: str) -> bool:
    """Delete personality profile."""
    try:
        filepath = os.path.join(config.PERSONALITIES_DIR, f"{name}.json")
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False
    except Exception:
        return False

def build_system_prompt(profile: dict) -> str:
    """Convert profile to system prompt."""
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
