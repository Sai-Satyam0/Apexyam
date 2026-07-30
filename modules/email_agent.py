
import urllib.parse
import streamlit as st
import config
import requests
import json


# =========================
# DRAFT EMAIL
# =========================

def draft_email(company: str, purpose: str) -> dict:
    """Draft professional email using Groq API."""

    try:

        if not company or not purpose:

            st.error(
                "Please provide both company name and purpose"
            )

            return None

        system_prompt = """
You are a professional email drafting assistant.

Return ONLY valid JSON in this exact format:

{
  "recipient_email": "...",
  "subject": "...",
  "body": "..."
}

Rules:
- Find the most likely HR/recruitment/public email of the company.
- If exact email is unknown, generate a realistic professional one.
- Keep the email concise and professional.
- No markdown.
- No extra text.
"""

        user_prompt = (
            f"Draft a professional email to {company} "
            f"regarding: {purpose}"
        )

        headers = {
            "Authorization": f"Bearer {config.GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": config.GROQ_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            "temperature": 0.5,
            "max_tokens": 500
        }

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        content = (
            data["choices"][0]["message"]["content"]
            .strip()
        )

        result = json.loads(content)

        return {

            "recipient_email": result.get(
                "recipient_email",
                f"hr@{company.lower().replace(' ', '')}.com"
            ),

            "subject": result.get(
                "subject",
                "Professional Inquiry"
            ),

            "body": result.get(
                "body",
                "Hello"
            )
        }

    except Exception as e:

        st.error(
            f"Email drafting error: {str(e)}"
        )

        return None


# =========================
# GMAIL LINK
# =========================

def get_gmail_link(
    recipient,
    subject,
    body
):

    return (
        "https://mail.google.com/mail/?view=cm&fs=1"
        f"&to={urllib.parse.quote(recipient)}"
        f"&su={urllib.parse.quote(subject)}"
        f"&body={urllib.parse.quote(body)}"
    )
