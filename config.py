import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
APP_PASSWORD = os.getenv("APP_PASSWORD")
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_FROM = os.getenv("TWILIO_PHONE_FROM")

DB_PATH = "apexyam.db"
GROQ_MODEL = "openai/gpt-oss-120b"
JAMENDO_CLIENT_ID=4403332f
TTS_VOICE = "en-US-JennyNeural"
FACE_DATA_DIR = "assets/face_data"
PERSONALITIES_DIR = "personalities"
HF_TOKEN = os.getenv("HF_TOKEN")
