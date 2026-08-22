import requests
import streamlit as st
import config


def cleanup_old_files():
    """No longer needed with Jamendo (no local downloads), kept for compatibility."""
    pass


def play(query: str) -> bool:
    """Search Jamendo for a track and stream it directly to the browser."""
    try:
        if not query.strip():
            st.error("Please enter a song name")
            return False

        if not config.JAMENDO_CLIENT_ID:
            st.error("Jamendo client_id is not configured. Add JAMENDO_CLIENT_ID to your environment variables.")
            return False

        params = {
            "client_id": config.JAMENDO_CLIENT_ID,
            "format": "json",
            "limit": 1,
            "search": query,
            "audioformat": "mp32",  # 192kbps mp3
        }

        response = requests.get(
            "https://api.jamendo.com/v3.0/tracks/",
            params=params,
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()

        results = data.get("results", [])
        if not results:
            st.error(f"No tracks found for '{query}' on Jamendo")
            return False

        track = results[0]
        audio_url = track.get("audio")

        if not audio_url:
            st.error("Track found but no audio URL available")
            return False

        # Fetch the actual audio bytes and stream them to the browser
        audio_response = requests.get(audio_url, timeout=30)
        audio_response.raise_for_status()

        st.audio(audio_response.content, format="audio/mp3", autoplay=True)

        track_name = track.get("name", query)
        artist_name = track.get("artist_name", "")
        st.caption(f"🎵 {track_name} — {artist_name}" if artist_name else f"🎵 {track_name}")

        return True

    except requests.exceptions.RequestException as e:
        st.error(f"Music error: {e}")
        return False
    except Exception as e:
        st.error(f"Music error: {e}")
        return False


def stop():
    """
    No-op: playback lives in the browser's <audio> element, which the server
    has no handle to. To let a user stop playback, track a 'now playing' flag
    in st.session_state and only render st.audio when it's set.
    """
    pass


def is_playing():
    """
    No longer meaningful server-side — playback state now lives in the
    browser. Track this via st.session_state if you need it in app logic.
    """
    return False
