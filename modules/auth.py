import streamlit as st
import config


def show_lock_screen():
    """Display password lock screen."""

    if st.session_state.get("authenticated", False):
        return True

    # ---------------- Header ---------------- #

    st.title("ApexYam")
    st.subheader("Your Intelligent AI Assistant")

    st.write(
        "A unified AI assistant capable of conversations, voice interaction, "
        "email automation, weather updates, chess, and persistent memory."
    )

    st.divider()

    # ---------------- Login ---------------- #

    left, center, right = st.columns([1, 2, 1])

    with center:

        st.subheader("Login")

        username = st.text_input(
            "Username",
            placeholder="Enter your username"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="lock_password",
            placeholder="Enter your password"
        )

        remember = st.checkbox("Remember this device")

        if st.button("Launch ApexYam", use_container_width=True):

            # Temporary authentication
            if (
                username == "admin"
                and password == config.APP_PASSWORD
            ):
                st.session_state.authenticated = True
                st.rerun()

            else:
                st.error("Incorrect username or password.")

    st.divider()

    # ---------------- Features ---------------- #

    st.subheader("What ApexYam Can Do")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("**Personality based Chat**")
        st.write("Can Switch to Customized personailty by you !!")

        st.info("**Voice Assistant**")
        st.write("Speech recognition and voice responses With realistic sound")

    with col2:
        st.info("**Email Agent**")
        st.write("Compose and send emails intelligently.")

        st.info("**Weather**")
        st.write("Get live weather updates instantly.")

    with col3:
        st.info("**Chess Engine**")
        st.write("Play against the built-in chess AI.")

        st.info("**Memory**")
        st.write("Stores conversations for context.")

    st.divider()

    st.header("Built With")

    tech1, tech2, tech3, tech4 = st.columns(4)

    tech1.metric("Frontend", "Streamlit")
    tech2.metric("Backend", "Python")
    tech3.metric("Database", "SQLite")
    tech4.metric("AI", "Groq Llama")

    st.divider()

    st.warning("Creater - Sai Satyam")

    st.stop()

    return False