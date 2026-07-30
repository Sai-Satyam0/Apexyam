import os
import tempfile
import threading
import asyncio
import pygame
import streamlit as st
import config
import speech_recognition as sr

# Initialize pygame mixer once
pygame.mixer.init()


def speak(text: str) -> None:
    """Convert text to speech and play it."""
    try:
        # Stop any existing audio
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

        # Generate TTS audio
        temp_file = os.path.join(tempfile.gettempdir(), "apexyam_tts.mp3")

        async def generate_tts():
            import edge_tts
            communicate = edge_tts.Communicate(text, config.TTS_VOICE)
            await communicate.save(temp_file)

        asyncio.run(generate_tts())

        # Play audio
        pygame.mixer.music.load(temp_file)
        pygame.mixer.music.play()

        # Wait for playback to finish
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)

    except Exception as e:
        st.error(f"Speech error: {str(e)}")


def speak_with_barge_in(text: str) -> str:
    """Speak text while listening for interruption. Returns user speech if interrupted."""
    try:
        # Stop any existing audio
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

        # Generate TTS audio
        temp_file = os.path.join(tempfile.gettempdir(), "apexyam_tts.mp3")

        async def generate_tts():
            import edge_tts
            communicate = edge_tts.Communicate(text, config.TTS_VOICE)
            await communicate.save(temp_file)

        asyncio.run(generate_tts())

        # Start playing audio in background thread
        interrupt_event = threading.Event()
        user_speech = [None]

        def play_audio():
            try:
                pygame.mixer.music.load(temp_file)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy() and not interrupt_event.is_set():
                    pygame.time.wait(50)
                if interrupt_event.is_set():
                    pygame.mixer.music.stop()
            except Exception:
                pass

        audio_thread = threading.Thread(target=play_audio)
        audio_thread.start()

        # Listen for interruption
        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                try:
                    audio = recognizer.listen(source, timeout=2, phrase_time_limit=3)
                    # If we got here, user spoke
                    interrupt_event.set()
                    pygame.mixer.music.stop()

                    try:
                        user_text = recognizer.recognize_google(audio)
                        user_speech[0] = user_text
                    except sr.UnknownValueError:
                        pass
                except sr.WaitTimeoutError:
                    pass  # No interruption
        except Exception:
            pass

        audio_thread.join(timeout=3)
        return user_speech[0]

    except Exception as e:
        st.error(f"Barge-in error: {str(e)}")
        return None
