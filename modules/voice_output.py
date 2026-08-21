import os
import tempfile
import asyncio
import streamlit as st
import config


def _generate_tts(text: str) -> str:
    """Generate TTS audio to a temp file and return its path."""
    temp_file = os.path.join(tempfile.gettempdir(), "apexyam_tts.mp3")

    async def generate_tts():
        import edge_tts
        communicate = edge_tts.Communicate(text, config.TTS_VOICE)
        await communicate.save(temp_file)

    asyncio.run(generate_tts())
    return temp_file


def speak(text: str) -> None:
    """Convert text to speech and play it in the user's browser."""
    try:
        temp_file = _generate_tts(text)

        with open(temp_file, "rb") as f:
            audio_bytes = f.read()

        # autoplay=True plays it immediately in the browser (no server-side wait needed)
        st.audio(audio_bytes, format="audio/mp3", autoplay=True)

    except Exception as e:
        st.error(f"Speech error: {str(e)}")


def speak_with_barge_in(text: str) -> str:
    """
    Speak text in the browser. NOTE: true 'barge-in' (interrupting playback by
    speaking) requires live microphone access from the browser while audio is
    playing, which pygame + SpeechRecognition can't do on a server — the
    server has no mic, and playback happens client-side now.

    This version just plays the audio. If you want real barge-in, you'd need
    a browser-based mic/audio component (e.g. streamlit-webrtc) so both
    playback and listening happen in the user's browser.
    """
    speak(text)
    return None
