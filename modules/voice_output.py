import os
import tempfile
import asyncio
import streamlit as st
import edge_tts
import config


def _run_async(coro):
    """
    Safely run an async coroutine whether or not an event loop exists.
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)

    new_loop = asyncio.new_event_loop()
    try:
        return new_loop.run_until_complete(coro)
    finally:
        new_loop.close()


async def _generate_tts(text: str, output_file: str):
    """
    Generate speech using Edge-TTS.
    """
    communicate = edge_tts.Communicate(
        text=text,
        voice=config.TTS_VOICE
    )
    await communicate.save(output_file)


def speak(text: str):
    """
    Convert text to speech and play it in the browser.
    """

    try:
        temp_file = os.path.join(
            tempfile.gettempdir(),
            "apexyam_tts.mp3"
        )

        _run_async(_generate_tts(text, temp_file))

        with open(temp_file, "rb") as audio:
            audio_bytes = audio.read()

        st.audio(
            audio_bytes,
            format="audio/mp3",
            autoplay=True
        )

    except Exception as e:
        st.error(f"Speech Error: {e}")


def speak_with_barge_in(text: str):
    """
    Streamlit version.

    Currently barge-in is not supported in the browser,
    so this simply speaks the text.
    """

    speak(text)
    return None
