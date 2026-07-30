import subprocess
import pygame
import streamlit as st
import os
import glob

pygame.mixer.init()

_current_audio = None
DOWNLOAD_DIR = "downloads"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def cleanup_old_files():
    files = glob.glob(f"{DOWNLOAD_DIR}/*")
    for f in files:
        try:
            os.remove(f)
        except:
            pass


def play(query: str) -> bool:
    global _current_audio

    try:
        if not query.strip():
            st.error("Please enter a song name")
            return False

        stop()
        cleanup_old_files()

        output_template = f"{DOWNLOAD_DIR}/song.%(ext)s"

        cmd = [
    "yt-dlp",
    "--extract-audio",
    "--audio-format", "mp3",
    "--ffmpeg-location", "/usr/bin",
    "--js-runtimes", "node",
    "-f", "bestaudio",
    "--no-playlist",
    "-o", output_template,
    f"ytsearch1:{query}"
]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode != 0:
            st.error(result.stderr)
            return False

        # Find downloaded file
        audio_files = glob.glob(f"{DOWNLOAD_DIR}/*.mp3")

        if not audio_files:
            st.error("Audio download failed")
            return False

        audio_path = audio_files[0]

        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()

        _current_audio = audio_path

        return True

    except subprocess.TimeoutExpired:
        st.error("Download timed out")
        return False

    except Exception as e:
        st.error(f"Music error: {e}")
        return False


def stop():
    global _current_audio

    try:
        pygame.mixer.music.stop()

        if _current_audio and os.path.exists(_current_audio):
            os.remove(_current_audio)

        _current_audio = None

    except:
        pass


def is_playing():
    try:
        return pygame.mixer.music.get_busy()
    except:
        return False