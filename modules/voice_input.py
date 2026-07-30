
import speech_recognition as sr
import streamlit as st

def listen_once() -> str:
    """Listen once from microphone and return transcribed text."""
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            st.sidebar.info("Listening...")

            recognizer.energy_threshold = 100
            recognizer.dynamic_energy_threshold = False

            try:
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=6)

            except sr.WaitTimeoutError:
                st.sidebar.error("No speech detected")
                return None

        st.sidebar.info("Processing...")
        text = recognizer.recognize_google(audio)
        st.sidebar.success(f"Heard: {text}")
        return text

    except sr.UnknownValueError:
        st.sidebar.error("Could not understand audio")
        return None

    except sr.RequestError as e:
        st.sidebar.error(f"Speech recognition error: {str(e)}")
        return None

    except Exception as e:
        st.sidebar.error(f"Microphone error: {str(e)}")
        return None

