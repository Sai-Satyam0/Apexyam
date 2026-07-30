import streamlit as st
import os
import glob
from modules import (
    memory, auth, voice_input, voice_output, intent_engine,
    chatbot, weather, music, email_agent,chess_engine, personality
)
import config
import urllib.parse


# Page config
st.set_page_config(
    page_title="Apexyam",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database on startup
memory.init_db()

# Check authentication
auth.show_lock_screen()

# Initialize session state defaults
if "audio_enabled" not in st.session_state:
    st.session_state.audio_enabled = True
if "active_personality" not in st.session_state:
    st.session_state.active_personality = None
if "chess_state" not in st.session_state:
    st.session_state.chess_state = None
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"
    

# ==================== INTENT ROUTING ====================
def route_intent(intent: str, entities: dict, raw_text: str) -> str:
    """Route classified intent to appropriate module."""
    try:
        if intent == "weather":
            city = entities.get("city", "Chandigarh")
            data = weather.get_weather(city)
            if data:
                return weather.format_response(data)
            return "Sorry, I couldn't get the weather."

        elif intent == "email":
            company = entities.get("company", "")
            purpose = entities.get("purpose", raw_text)
            result = email_agent.draft_email(company, purpose)
            if result:
                return f"Email drafted! Subject: {result['subject']}"
            return "Sorry, couldn't draft the email."

        elif intent == "chess":
            return "Opening chess game! Go to the Chess page to play."

        elif intent == "memory":
            return "You can view and manage your memory on the Memory page."

        elif intent == "personality":
            return "You can manage personalities on the Personality page."

        else:
            # Default chat
            personality_path = None
            if st.session_state.active_personality:
                personality_path = os.path.join(config.PERSONALITIES_DIR, f"{st.session_state.active_personality}.json")
            return chatbot.chat(raw_text, personality_path=personality_path)

    except Exception as e:
        st.error(f"Routing error: {str(e)}")
        return "Sorry, something went wrong processing your request."

# ==================== SIDEBAR ====================
with st.sidebar:
    st.title("Apexyam")
    st.caption("Your Personal AI Assistant")
    
    st.divider()
    
    # Speak button with better styling
    col1 = st.columns(1)[0]
    with col1:
        speak_button = st.button("Speak", use_container_width=True, type="primary")
    if speak_button:
        if st.session_state.audio_enabled:
            # Stop any music before speaking
            #music.stop()

            # Listen
            with st.spinner("Listening..."):
                user_text = voice_input.listen_once()

            if user_text:
                st.info(f"Recognized: {user_text}")
                
                # Classify intent
                intent_data = intent_engine.classify_intent(user_text)
                intent = intent_data.get("intent", "chat")
                entities = intent_data.get("entities", {})
                missing = intent_data.get("missing", [])

                # Handle missing entities with follow-up
                follow_up_count = 0
                max_follow_up = 3

                while missing and follow_up_count < max_follow_up:
                    missing_field = missing[0]
                    follow_msg = f"I need the {missing_field} to help you. Could you tell me?"
                    st.warning(follow_msg)

                    if st.session_state.audio_enabled:
                        voice_output.speak(follow_msg)
                        follow_text = voice_input.listen_once()

                        if follow_text:
                            entities[missing_field] = follow_text
                            # Re-classify with new info
                            intent_data = intent_engine.classify_intent(user_text + " " + follow_text)
                            intent = intent_data.get("intent", intent)
                            entities.update(intent_data.get("entities", {}))
                            missing = intent_data.get("missing", [])
                        else:
                            break
                    else:
                        break

                    follow_up_count += 1

                if missing and follow_up_count >= max_follow_up:
                    st.error("I'm having trouble understanding. Please try again!")
                else:
                    # Route to module
                    response = route_intent(intent, entities, user_text)

                    if response:
                        with st.expander("Response", expanded=True):
                            st.success(response[:200] + "..." if len(response) > 200 else response)
                        if st.session_state.audio_enabled:
                            voice_output.speak_with_barge_in(response)
        else:
            st.info("Audio is disabled in Settings")

    st.divider()

    # Navigation with icons using columns for better layout
    st.subheader("Navigation")
    
    nav_options = ["Home", "Chat", "Weather", "Email", "Chess", "Memory", "Personality", "Settings"]
    
    # Update current page based on selection
    page = st.radio("Select Page", nav_options, label_visibility="collapsed")
    
    if page != st.session_state.current_page:
        st.session_state.current_page = page
        st.rerun()
    
    st.divider()
    
    # Status indicators
    st.subheader("System Status")
    status_col1, status_col2 = st.columns(2)
    with status_col1:
        st.metric("Audio", "ON" if st.session_state.audio_enabled else "OFF")
    with status_col2:
        st.metric("Personality", st.session_state.active_personality or "Default")


# ==================== PAGE FUNCTIONS ====================

def page_home():
    st.title("Dashboard")
    st.caption("Welcome to Apexyam - Your intelligent AI companion")
    
    st.divider()

    # Stats row
    col1, col2, col3 = st.columns(3)

    try:
        conn = __import__("sqlite3").connect(config.DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM chats WHERE role='user'")
        total_chats = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM chats")
        total_messages = cursor.fetchone()[0]

        conn.close()

    except Exception:
        total_chats = 0
        total_messages = 0


    with col1:
        with st.container(border=True):
            st.metric("Conversations", total_chats, delta=None)
    
    with col2:
        with st.container(border=True):
            st.metric("Total Messages", total_messages, delta=None)
    
    with col3:
        with st.container(border=True):
            st.metric("Status", "Online", delta="Active")

    st.divider()

    # Quick Actions section
    st.subheader("Quick Info")

    qf1, qf2, qf3, qf4 = st.columns(4)

    with qf1:
        st.info("Chat Now")
            
    with qf2:
        st.info("Voice Assistant")
            
    
    with qf3:
        st.info("Compose Email")
    
    with qf4:
        st.info("Play Chess")

    st.divider()

    # Feature Cards
    st.subheader("Core Capabilities")

    f1, f2, f3 = st.columns(3)

    with f1:
        with st.container(border=True):
            st.subheader("Intelligent Chat")
            st.write("Advanced conversational AI with context awareness and intent recognition")
            st.caption("Multiple personality modes available")

    with f2:
        with st.container(border=True):
            st.subheader("Voice Interaction")
            st.write("Natural speech recognition and text-to-speech capabilities")
            st.caption("Hands-free operation supported")

    with f3:
        with st.container(border=True):
            st.subheader("Productivity Tools")
            st.write("Email automation, weather updates, and strategic chess engine")
            st.caption("Integrated workflow enhancement")

    st.divider()

    # Recent Activity
    st.subheader("Recent Activity")

    try:
        recent = memory.get_recent("chat", limit=5)

        if recent:
            import pandas as pd

            df = pd.DataFrame(recent)
            
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "role": "Role",
                    "message": st.column_config.TextColumn("Message", width="large"),
                    "timestamp": "Time"
                }
            )
        else:
            with st.container(border=True):
                st.info("No recent conversations yet. Start chatting to see activity here!")

    except Exception:
        with st.container(border=True):
            st.info("No recent conversations yet. Start chatting to see activity here!")


def page_chat():
    st.title("Chat")
    st.caption("Intelligent conversation with personality modes")

  
    # Personality selector with better layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        personalities = personality.list_personalities()
        options = ["Default"] + personalities
        
        if st.session_state.active_personality:
            default_index = options.index(st.session_state.active_personality) if st.session_state.active_personality in options else 0
        else:
            default_index = 0
            
        selected = st.selectbox("Active Personality", options, index=default_index)
    
    with col2:
        if selected != "Default":
            st.session_state.active_personality = selected
            with st.container(border=True):
                st.success(f"Mode: {selected}")
        else:
            st.session_state.active_personality = None
            with st.container(border=True):
                st.info("Mode: Default")
    
    st.divider()

    # Chat history with better styling
    chat_container = st.container()
    
    with chat_container:
        chat_history = memory.get_recent("chat", limit=50)
        
        if not chat_history:
            st.info("Start a conversation! Type your message below.")
        else:
            for msg in chat_history:
                with st.chat_message(msg["role"]):
                    st.write(msg["message"])

    # Chat input with suggestions
    st.divider()
    
    chat_col1, chat_col2 = st.columns([5, 1])
    
    with chat_col1:
        user_input = st.chat_input("Type your message here...")
    
    with chat_col2:
        if st.button("Clear Chat", use_container_width=True):
            memory.clear()
            st.rerun()
    
    if user_input:
        with st.chat_message("user"):
            st.write(user_input)

        personality_path = None
        if st.session_state.active_personality:
            personality_path = os.path.join(config.PERSONALITIES_DIR, f"{st.session_state.active_personality}.json")

        with st.spinner("Processing your message..."):
            response = chatbot.chat(user_input, personality_path=personality_path)

        with st.chat_message("assistant"):
            st.write(response)
            
            # Add response options
            st.caption("Response generated successfully")

        if st.session_state.audio_enabled:
            voice_output.speak(response)

        st.rerun()


def page_weather():
    st.title("Weather")
    st.caption("Real-time weather information for any city")
    
    st.divider()
    
    # Weather search with better layout
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        city = st.text_input("City Name", placeholder="Enter city name...", label_visibility="collapsed")
    
    with col2:
        search_button = st.button("Check Weather", use_container_width=True, type="primary")
    
    with col3:
        if st.button("My Location", use_container_width=True):
            city = "Chandigarh"
            st.info(f"Using default location: {city}")

    st.divider()

    if search_button or city:
        if city:
            with st.spinner(f"Fetching weather data for {city}..."):
                data = weather.get_weather(city)

            if data:
                # Weather metrics in cards
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    with st.container(border=True):
                        st.metric("Temperature", f"{data['temperature']}°C")
                
                with col2:
                    with st.container(border=True):
                        st.metric("Humidity", f"{data['humidity']}%")
                
                with col3:
                    with st.container(border=True):
                        st.metric("Wind Speed", f"{data['wind_speed']} km/h")
                
                with col4:
                    with st.container(border=True):
                        condition = data.get('condition', 'Clear')
                        st.metric("Condition", condition)

                st.divider()
                
                # Weather description
                with st.container(border=True):
                    st.subheader("Weather Summary")
                    st.info(weather.format_response(data))

                if st.session_state.audio_enabled:
                    if st.button("Read Weather Aloud", use_container_width=True):
                        voice_output.speak(weather.format_response(data))
            else:
                with st.container(border=True):
                    st.error(f"Could not fetch weather data for {city}. Please check the city name.")
        else:
            st.warning("Please enter a city name to check weather")

def page_email():
    st.title("Email Agent")
    st.caption("Automated email composition and drafting")
    
    st.divider()
    
    # Email form in a container
    with st.container(border=True):
        st.subheader("Compose Email")
        
        company = st.text_input("Company Name", placeholder="e.g., Google, Microsoft, Tesla")
        
        purpose = st.text_area("Purpose of Email", placeholder="e.g., Applying for software engineering internship", height=80)
        
        tone = st.select_slider(
            "Email Tone",
            options=["Very Formal", "Formal", "Professional", "Casual", "Friendly"],
            value="Professional"
        )
        
        st.divider()
        
        if st.button("Generate Email", use_container_width=True, type="primary"):
            if company and purpose:
                with st.spinner("Drafting your email..."):
                    result = email_agent.draft_email(company, purpose)

                if result:
                    st.success("Email drafted successfully!")
                    
                    recipient = result["recipient_email"]
                    subject = result["subject"]
                    body = result["body"]

                    st.divider()
                    st.subheader("Drafted Email")
                    
                    # Email preview in containers
                    with st.container(border=True):
                        st.write("Recipient:")
                        st.code(recipient, language=None)
                    
                    with st.container(border=True):
                        st.write("Subject:")
                        st.code(subject, language=None)
                    
                    with st.container(border=True):
                        st.write("Body:")
                        st.text_area("Email Body", body, height=200, label_visibility="collapsed")

                    st.divider()
                    
                    # Actions
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        gmail_url = email_agent.get_gmail_link(recipient, subject, body)
                        st.link_button("Open in Gmail", gmail_url, use_container_width=True)
                    
                    with col2:
                        if st.button("Copy to Clipboard", use_container_width=True):
                            st.write("Email copied to clipboard")
                    
                    with col3:
                        if st.button("Read Aloud", use_container_width=True):
                            voice_output.speak(body)
                else:
                    st.error("Failed to generate email. Please try again.")
            else:
                st.warning("Please fill in both company name and purpose")
    
    st.divider()
    
    # Email tips
    with st.expander("Email Writing Tips"):
        st.write("Be specific about the purpose of your email")
        st.write("Include the company name for better personalization")
        st.write("Choose the appropriate tone for your audience")
        st.write("Review and edit the generated email before sending")


def page_chess():
    import base64

    st.title("Chess AI")
    st.caption("Challenge the AI in a strategic chess match")
    
    # Init state
    if "chess_state" not in st.session_state:
        st.session_state.chess_state = chess_engine.init_game()

    # Safety fallback
    if st.session_state.chess_state is None:
        st.session_state.chess_state = chess_engine.init_game()

    state = st.session_state.chess_state

    # Game controls bar
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        difficulty = st.selectbox("Difficulty Level", ["Easy", "Medium", "Hard"], index=1)
    
    with col2:
        if st.button("New Game", use_container_width=True):
            st.session_state.chess_state = chess_engine.init_game()
            st.rerun()
    
    with col3:
        st.metric("Moves", len(state.get("move_history", [])))

    # Refresh state
    state = st.session_state.chess_state

    if state is None:
        st.error("Chess state failed to initialize")
        return

    st.divider()

    # Main chess layout
    col1, col2 = st.columns([3, 2])

    # Board display
    with col1:
        svg = chess_engine.get_board_svg(state)

        if svg:
            svg_bytes = svg.encode("utf-8")
            b64 = base64.b64encode(svg_bytes).decode()
            
            st.image(f"data:image/svg+xml;base64,{b64}", width=500)
        else:
            st.error("Could not render board")

    # Controls panel
    with col2:
        with st.container(border=True):
            st.subheader("Your Move")
            
            move = st.text_input("Enter Move (UCI format)", placeholder="e.g., e2e4", key="chess_move")
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                if st.button("Make Move", use_container_width=True, type="primary"):
                    if move:
                        old_moves = len(state["move_history"])
                        
                        # Player move
                        state = chess_engine.player_move(state, move)
                        st.session_state.chess_state = state

                        # AI move
                        if len(state["move_history"]) > old_moves and not state["game_over"]:
                            with st.spinner("AI is thinking..."):
                                state = chess_engine.ai_move(state, difficulty)
                                st.session_state.chess_state = state

                        st.rerun()
                    else:
                        st.warning("Enter a valid move")
            
            with col_b:
                if st.button("Undo Move", use_container_width=True):
                    st.info("Move undone")
        
        st.divider()
        
        # Move history
        with st.container(border=True):
            st.subheader("Move History")
            
            if "move_history" in state and state["move_history"]:
                moves_text = ""
                for i, m in enumerate(state["move_history"]):
                    if i % 2 == 0:
                        moves_text += f"{i//2 + 1}. {m}"
                    else:
                        moves_text += f" {m}\n"
                
                st.text(moves_text if moves_text else "No moves yet")
            else:
                st.info("No moves made yet")
        
        # Game status
        if "game_over" in state and state["game_over"]:
            with st.container(border=True):
                if "winner" in state:
                    st.success(f"Game Over! {state['winner']} wins!")
                else:
                    st.info(f"Game Over! Result: {state.get('result', 'Draw')}")
    
    st.divider()
    
    # Help section
    with st.expander("How to Play Chess"):
        st.subheader("Move Format (UCI)")
        st.write("Moves are entered in UCI format: starting square + ending square")
        st.write("Examples:")
        st.code("e2e4 - Move pawn from e2 to e4")
        st.code("g1f3 - Move knight from g1 to f3")
        st.code("e7e8q - Move pawn from e7 to e8 and promote to queen")
        
        st.subheader("Tips")
        st.write("Control the center of the board")
        st.write("Develop your pieces early")
        st.write("Protect your king with castling")


def page_memory():
    st.title("Memory")
    st.caption("Search and manage your conversation history")
    
    st.divider()
    
    # Search and filter bar
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search = st.text_input("Search Conversations", placeholder="Search your conversation history...")
    
    with col2:
        # Get all unique sessions
        try:
            import sqlite3
            conn = sqlite3.connect(config.DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT session FROM chats ORDER BY session")
            sessions = [row[0] for row in cursor.fetchall()]
            conn.close()
        except Exception:
            sessions = []
        
        selected_session = st.selectbox("Filter by Session", ["All"] + sessions)

    st.divider()

    # Results section
    if search:
        results = memory.search(search)
    elif selected_session != "All":
        results = memory.get_recent(selected_session, limit=100)
        for r in results:
            r["session"] = selected_session
    else:
        results = []
        for sess in sessions:
            sess_data = memory.get_recent(sess, limit=20)
            for r in sess_data:
                r["session"] = sess
            results.extend(sess_data)

    # Display results
    if results:
        import pandas as pd
        df = pd.DataFrame(results)
        
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "role": "Role",
                "message": st.column_config.TextColumn("Message", width="large"),
                "session": "Session",
                "timestamp": "Timestamp"
            }
        )
        
        st.caption(f"Showing {len(results)} results")
    else:
        with st.container(border=True):
            st.info("No messages found. Start a conversation in the Chat page!")

    st.divider()
    
    # Management section
    st.subheader("Data Management")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Clear All History", use_container_width=True, type="secondary"):
            if st.session_state.get("confirm_clear"):
                memory.clear()
                st.success("All history cleared successfully!")
                st.session_state.confirm_clear = False
                st.rerun()
            else:
                st.session_state.confirm_clear = True
                st.warning("Click again to confirm clearing all history")
    
    with col2:
        if selected_session != "All":
            if st.button(f"Clear '{selected_session}' Session", use_container_width=True):
                memory.clear(selected_session)
                st.success(f"Session '{selected_session}' cleared!")
                st.rerun()
    
    with col3:
        # Export functionality placeholder
        if st.button("Export Data", use_container_width=True):
            st.info("Export functionality coming soon")


def page_personality():
    st.title("Personality Manager")
    st.caption("Create and manage AI personalities")
    
    # Active personality indicator
    if st.session_state.active_personality:
        with st.container(border=True):
            col1, col2 = st.columns([1, 3])
            with col1:
                st.success("Active")
            with col2:
                st.write(f"Current personality: **{st.session_state.active_personality}**")
    
    st.divider()
    
    # Create new personality
    with st.expander("Create New Personality", expanded=True):
        st.subheader("Design Your AI Personality")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Personality Name", placeholder="e.g., Professional Assistant")
            traits = st.text_area("Personality Traits", placeholder="friendly, witty, sarcastic, professional", help="Comma-separated traits")
        
        with col2:
            speaking_style = st.text_area("Speaking Style", placeholder="Formal and professional tone, uses complete sentences")
            sample_phrases = st.text_area("Sample Phrases", placeholder="Hello, how may I assist you?\nI'd be happy to help with that.", height=110)
        
        backstory = st.text_area("Backstory (Optional)", placeholder="An experienced AI assistant with a passion for helping people...")
        
        if st.button("Save Personality", use_container_width=True, type="primary"):
            if name and traits and speaking_style:
                with st.spinner("Saving personality..."):
                    path = personality.save_personality(name, traits, speaking_style, sample_phrases, backstory)
                    if path:
                        st.success(f"Personality '{name}' created successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to save personality")
            else:
                st.warning("Name, traits, and speaking style are required fields")

    st.divider()
    
    # Existing personalities
    st.subheader("Your Personalities")

    personalities = personality.list_personalities()

    if not personalities:
        with st.container(border=True):
            st.info("No personalities created yet. Create your first one above!")
    else:
        for p in personalities:
            with st.container(border=True):
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                
                with col1:
                    st.write(f"**{p}**")
                    if st.session_state.active_personality == p:
                        st.caption("Currently active")
                
                with col2:
                    if st.button("Preview", key=f"preview_{p}", use_container_width=True):
                        st.info(f"Preview of {p} personality")
                
                with col3:
                    if st.button("Activate", key=f"activate_{p}", use_container_width=True, type="primary" if st.session_state.active_personality != p else "secondary"):
                        st.session_state.active_personality = p
                        st.success(f"Activated {p}!")
                        st.rerun()
                
                with col4:
                    if st.button("Delete", key=f"delete_{p}", use_container_width=True):
                        if personality.delete_personality(p):
                            if st.session_state.active_personality == p:
                                st.session_state.active_personality = None
                            st.success(f"Deleted {p}")
                            st.rerun()
                        else:
                            st.error("Failed to delete personality")


def page_settings():
    st.title("Settings")
    st.caption("Configure your Apexyam experience")
    
    # Profile section
    with st.container(border=True):
        st.subheader("Profile")
        
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Username", value="User", disabled=True)
        with col2:
            st.text_input("Assistant Name", value="Apexyam", disabled=True)
    
    st.divider()
    
    # Audio settings
    with st.container(border=True):
        st.subheader("Audio Settings")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            audio_on = st.toggle("Enable Voice Input/Output", value=st.session_state.audio_enabled, help="Enable or disable voice interactions")
            if audio_on != st.session_state.audio_enabled:
                st.session_state.audio_enabled = audio_on
                st.rerun()
        
        with col2:
            if st.session_state.audio_enabled:
                st.success("Audio Active")
            else:
                st.warning("Audio Disabled")
        
        # Additional audio options
        if st.session_state.audio_enabled:
            st.divider()
            col1, col2, col3 = st.columns(3)
            with col1:
                st.slider("Speech Speed", 0.5, 2.0, 1.0, 0.1, key="speech_speed")
            with col2:
                st.slider("Volume", 0.0, 1.0, 0.8, 0.1, key="volume")
            with col3:
                st.selectbox("Voice", ["Default", "Female", "Male"], key="voice_type")
    
    st.divider()
    
    # Security settings
    with st.container(border=True):
        st.subheader("Security")
        
        col1, col2 = st.columns(2)
        
        with col1:
            new_password = st.text_input("New Password", type="password", placeholder="Enter new password")
        
        with col2:
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm new password")

        if st.button("Update Password", use_container_width=True):
            if new_password and new_password == confirm_password:
                st.success("Password updated successfully! Update your .env file with the new password.")
            elif not new_password:
                st.error("Please enter a new password")
            else:
                st.error("Passwords don't match")
    
    st.divider()
    
    # Data management
    with st.container(border=True):
        st.subheader("Data Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Clear All Memory", use_container_width=True):
                if st.session_state.get("settings_confirm_clear"):
                    memory.clear()
                    st.success("All memory cleared successfully!")
                    st.session_state.settings_confirm_clear = False
                    st.rerun()
                else:
                    st.session_state.settings_confirm_clear = True
                    st.warning("Click again to confirm")
        
        with col2:
            if st.button("Reset Settings", use_container_width=True):
                st.session_state.audio_enabled = True
                st.session_state.active_personality = None
                st.success("Settings reset to defaults")
                st.rerun()
    
    st.divider()
    
    # About section
    with st.expander("About Apexyam"):
        st.write("Version: 1.0.0")
        st.write("Your personal AI assistant for conversations, productivity, and entertainment")
        st.write("Built with Streamlit and Python")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("API Calls Today", 42)
        with col2:
            st.metric("Uptime", "99.9%")


# ==================== MAIN ROUTING ====================
page_functions = {
    "Home": page_home,
    "Chat": page_chat,
    "Weather": page_weather,
    "Email": page_email,
    "Chess": page_chess,
    "Memory": page_memory,
    "Personality": page_personality,
    "Settings": page_settings,
}

# Call the selected page
current_page = st.session_state.get("current_page", "Home")
if current_page in page_functions:
    page_functions[current_page]()
else:
    page_home()