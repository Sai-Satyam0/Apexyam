import subprocess
import streamlit as st
import os
import glob

DOWNLOAD_DIR = "downloads"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def cleanup_old_files():
    files = glob.glob(f"{DOWNLOAD_DIR}/*")
    for f in files:
        try:
            os.remove(f)
        except Exception:
            pass


def play(query: str) -> bool:
    try:
        if not query.strip():
            st.error("Please enter a song name")
            return False

        cleanup_old_files()

        output_template = f"{DOWNLOAD_DIR}/song.%(ext)s"

        cmd = [
            "yt-dlp",
            "--extract-audio",
            "--audio-format", "mp3",
            "--ffmpeg-location", "/usr/bin",
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

        with open(audio_path, "rb") as f:
            audio_bytes = f.read()

        # Plays in the user's browser, not on the server
        st.audio(audio_bytes, format="audio/mp3", autoplay=True)

        return True

    except subprocess.TimeoutExpired:
        st.error("Download timed out")
        return False

    except Exception as e:
        st.error(f"Music error: {e}")
        return False


def stop():
    """
    No-op now: playback lives in the browser's <audio> element (rendered by
    st.audio), which the server has no handle to. To let a user stop playback,
    add a stop/replace control in the UI itself (e.g. only render st.audio
    when a 'now playing' flag is set in st.session_state, and clear that flag
    on a Stop button click).
    """
    cleanup_old_files()


def is_playing():
    """
    No longer meaningful server-side — playback state now lives in the
    browser. If you need to track this in your app logic, use
    st.session_state (e.g. set a flag when you call play(), clear it on stop()).
    """
    return False
