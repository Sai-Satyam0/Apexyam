# ApexYam

ApexYam is an AI-powered personal assistant built using Python and Streamlit. It combines conversational AI with productivity features such as voice interaction, AI-powered email generation, weather updates, music playback, personality customization, memory management, and a chess engine within a single application.

The goal of this project is to demonstrate how multiple AI-driven utilities can be integrated into a unified and user-friendly web application.

**Live Demo:** [apexyam-1.onrender.com](https://apexyam-1.onrender.com/)

**Demo Login**
```
Username: admin
Password: SaiSatyam
```

Note: the app runs on a free Render instance, so it may take up to 50 seconds to wake up on the first visit after a period of inactivity.

A demonstration is also available via the screenshots below.

---

# Table of Contents

- Overview
- Features
- Application Screenshots
- Technology Stack
- Project Structure
- Installation
- Environment Variables
- How It Works
- Future Improvements
- Author

---

# Overview

Modern AI assistants often focus on a single capability such as chatting, voice interaction, or automation. ApexYam brings these capabilities together into one application.

The application is designed with a modular architecture where each feature is implemented independently, making it easier to maintain, extend, and improve over time.

The interface is built with Streamlit while the backend is implemented entirely in Python, and the entire app is deployed as a live web service.

---

# Features

## AI Assistant

- Natural language conversations
- Fast AI responses powered by the Groq API
- Context-aware interactions

---

## Voice Interaction

- Browser-based microphone recording (works fully in the cloud, no local hardware required)
- Speech-to-text transcription
- Text-to-speech responses played back directly in the browser

---

## Email Assistant

- Generate professional emails using AI
- Convert prompts into complete email drafts

---

## Weather Information

- Real-time weather updates
- City-based weather search

---

## Music Playback

- Search and stream independent, royalty-free tracks via the Jamendo API
- Simple command-based interface

---

## Chess Engine

- Play against the Stockfish chess engine
- Interactive chess board

---

## Personality Management

- Multiple assistant personalities
- Easy personality switching

---

## Memory Management

- Store and retrieve conversation history
- Better contextual responses

---

## Secure Authentication

- Password protected login
- Environment variable based configuration

---

# Application Screenshots

## Login Page

Secure authentication before accessing the assistant.

![Login Page](Apexyam_Images/Login_Page.png)

---

## Dashboard

The main interface providing access to all available features.

![Dashboard](Apexyam_Images/Dashboard.png)

---

## AI Chat

Interact naturally with the AI assistant.

![Chat Interface](Apexyam_Images/Chat.png)

---

## Weather Module

Retrieve current weather information for any city.

![Weather](Apexyam_Images/Weather.png)

---

## Email Generation

Provide a simple prompt.

![Email Command](Apexyam_Images/Email_command.png)

Generated email output.

![Email Result](Apexyam_Images/Email_Command_result.png)

---

## Chess Module

Play chess against the integrated Stockfish engine.

![Chess](Apexyam_Images/Chess.png)

---

## Memory Manager

View stored conversations and memory.

![Memory](Apexyam_Images/Memory.png)

---

## Personality Manager

Switch between different AI personalities.

![Personality](Apexyam_Images/Personality.png)

---

# Technology Stack

## Frontend

- Streamlit

## Backend

- Python

## AI

- Groq API (openai/gpt-oss-120b)

## Deployment

- Render (Web Service)

## Libraries

- Requests
- SpeechRecognition
- streamlit-mic-recorder
- Edge-TTS
- python-chess
- Stockfish
- bcrypt
- pandas
- python-dotenv

---

## project structure

ApexYam/
│
├── app.py                     # Main Streamlit application & page routing
├── config.py                  # Environment variable loading & app settings
├── requirements.txt           # Python dependencies
├── runtime.txt                # Pinned Python version for deployment
├── README.md
├── .env.example                # Template for required environment variables
├── .gitignore
│
├── assets/                    # Static assets used by the app
│
├── modules/                   # Core application logic, one file per feature
│   ├── auth.py                 # Login / lock screen authentication
│   ├── chatbot.py               # Groq-powered conversational AI
│   ├── chess_engine.py          # Stockfish integration & board state
│   ├── email_agent.py           # AI-generated email drafting
│   ├── intent_engine.py         # Classifies voice commands into intents
│   ├── memory.py                # SQLite-backed conversation history
│   ├── music.py                 # Jamendo API search & playback
│   ├── personality.py           # Custom AI personality profiles
│   ├── voice_input.py           # Browser microphone recording & transcription
│   ├── voice_output.py          # Text-to-speech playback
│   └── weather.py               # Live weather lookups
│
├── personalities/              # Saved custom personality JSON profiles
│
└── Apexyam_Images/             # Screenshots used in this README

---

# Installation

Clone the repository.

```bash
git clone https://github.com/Sai-Satyam0/ApexYam.git
```

Move into the project directory.

```bash
cd ApexYam
```

Install all dependencies.

```bash
pip install -r requirements.txt
```

Create a `.env` file using the provided `.env.example`.

Run the application.

```bash
streamlit run app.py
```

---

# Environment Variables

Create a `.env` file and configure the following variables.

```env
GROQ_API_KEY=

APP_PASSWORD=

SMTP_EMAIL=

SMTP_PASSWORD=

TWILIO_ACCOUNT_SID=

TWILIO_AUTH_TOKEN=

TWILIO_PHONE_FROM=

HF_TOKEN=

JAMENDO_CLIENT_ID=
```

For a live deployment, these same variables must also be added to your hosting platform's environment settings (e.g. Render's Environment tab) — the `.env` file itself is never uploaded to GitHub or the server.

---

# How It Works

1. User authentication is performed at login.
2. The dashboard provides access to different assistant modules.
3. User requests are processed by individual modules.
4. AI requests are sent to the Groq API.
5. Responses are displayed through the Streamlit interface, with voice responses played back in the browser.
6. Additional modules handle email generation, weather information, voice interaction, music playback, chess gameplay, and memory management.

---

# Future Improvements

- Image generation
- File summarization
- Plugin architecture
- Multi-language support
- Cloud synchronization
- Multiple user profiles
- Mobile-friendly interface

---

# Author

Developed by **Sai Satyam**

This project was created as part of my learning journey in Python, artificial intelligence, and application development. It reflects my interest in building practical AI-powered software with clean interfaces and modular architecture.
