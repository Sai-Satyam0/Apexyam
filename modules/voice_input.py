import io
import streamlit as st
import speech_recognition as sr
from streamlit_mic_recorder import mic_recorder


def listen_once() -> str:
    """
    Record audio from the user's BROWSER microphone (not the server) and
    return transcribed text.

    Renders a record widget. The user clicks to start, speaks, clicks to
    stop. The recorded audio is sent from the browser to this app, then
    transcribed with SpeechRecognition.

    NOTE: unlike the old local-mic version, this requires a UI interaction
    and a Streamlit rerun to get the audio back — it can't be called
    multiple times in a row inside one button handler and block until each
    finishes. Each call renders its own recorder widget.
    """
    audio = mic_recorder(
        start_prompt="🎤 Start Recording",
        stop_prompt="⏹ Stop Recording",
        just_once=True,
        use_container_width=True,
        format="wav",
        key="voice_input_recorder",
    )

    if audio is None:
        return None

    audio_bytes = audio["bytes"]

    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
            audio_data = recognizer.record(source)

        st.sidebar.info("Processing...")
        text = recognizer.recognize_google(audio_data)
        st.sidebar.success(f"Heard: {text}")
        return text

    except sr.UnknownValueError:
        st.sidebar.error("Could not understand audio")
        return None

    except sr.RequestError as e:
        st.sidebar.error(f"Speech recognition error: {str(e)}")
        return None

    except Exception as e:
        st.sidebar.error(f"Audio processing error: {str(e)}")
        return None
