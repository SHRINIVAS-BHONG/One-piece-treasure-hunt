# streamlit_app.py
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from graph import create_graph
from state import ChatState
from utils import check_riddle_solution
import random

# ---------- Page config ----------
st.set_page_config(
    page_title="One Piece: Treasure Hunt",
    page_icon="🏴‍☠️",  # Pirate flag icon
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- Custom CSS: CRT, scanlines, matrix rain ----------
CRT_CSS = """
<style>
/* Import a pixel-style mono font */
@import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');

:root{
  --neon-green: #39ff14;
  --electric-blue: #00d0ff;
  --magenta: #ff00ff;
  --cyber-purple: #a456f0;
}

html, body, [class*="block-container"]{
  background: #000000 !important;
  padding: 0;
  margin: 0;
}

* { 
    font-family: 'VT323', monospace; 
    letter-spacing: .4px; 
}

/* Hide default Streamlit elements */
header, footer, .stChatInputContainer {
    visibility: hidden;
    height: 0;
}

/* Main container */
.main {
    padding: 0;
    margin: 0;
    height: 100vh;
    display: flex;
    flex-direction: column;
}

/* CRT scanline effect overlay */
.main::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: repeating-linear-gradient(
        0deg,
        rgba(0, 0, 0, 0.15),
        rgba(0, 0, 0, 0.15) 1px,
        transparent 1px,
        transparent 2px
    );
    pointer-events: none;
    z-index: 100;
}

/* Glitch effect for text */
@keyframes glitch {
    0% { transform: translate(0); }
    20% { transform: translate(-2px, 2px); }
    40% { transform: translate(-2px, -2px); }
    60% { transform: translate(2px, 2px); }
    80% { transform: translate(2px, -2px); }
    100% { transform: translate(0); }
}

.glitch-text {
    animation: glitch 0.5s infinite;
}

/* Header section */
.header {
    text-align: center;
    padding: 10px 0;
    margin-bottom: 10px;
    border-bottom: 2px solid var(--neon-green);
}

.title {
    font-size: 42px;
    text-transform: uppercase;
    color: var(--neon-green);
    text-shadow: 0 0 10px rgba(57,255,20,.9), 0 0 20px rgba(57,255,20,.6);
    margin: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 15px;
}

.pirate-flag {
    font-size: 36px;
    animation: rotate 5s infinite linear;
}

@keyframes rotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

/* Chat container */
.chat-container {
    flex: 1;
    overflow-y: auto;
    padding: 10px 20px;
    margin-bottom: 70px;
    display: flex;
    flex-direction: column;
    gap: 15px;
}

/* Message bubbles */
.message {
    max-width: 70%;
    padding: 12px 15px;
    border-radius: 10px;
    position: relative;
}

.message.ai {
    align-self: flex-start;
    background: rgba(57,255,20,0.15);
    border: 1px solid var(--neon-green);
    border-left: 5px solid var(--neon-green);
    margin-right: auto;
}

.message.user {
    align-self: flex-end;
    background: rgba(255,255,255,0.1);
    border: 1px solid var(--electric-blue);
    border-right: 5px solid var(--electric-blue);
    margin-left: auto;
}

.message .role {
    font-size: 16px;
    opacity: 0.8;
    margin-bottom: 5px;
    text-transform: uppercase;
}

.message .content {
    font-size: 20px;
    white-space: pre-wrap;
}

.message.ai .content {
    color: var(--neon-green);
    text-shadow: 0 0 5px rgba(57,255,20,.6);
}

.message.user .content {
    color: var(--electric-blue);
    text-shadow: 0 0 5px rgba(0,208,255,.3);
}

/* Input container */
.input-container {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 15px;
    background: rgba(0, 0, 0, 0.9);
    border-top: 2px solid var(--magenta);
    z-index: 1000;
}

.input-wrapper {
    display: flex;
    gap: 10px;
}

.custom-input {
    flex: 1;
    background: transparent;
    border: 1px solid var(--magenta);
    color: var(--magenta);
    padding: 12px;
    font-size: 18px;
    font-family: 'VT323', monospace;
}

.custom-input:focus {
    outline: none;
    box-shadow: 0 0 8px var(--magenta);
}

.send-button {
    background: var(--magenta);
    color: #000;
    border: none;
    padding: 0 20px;
    font-size: 18px;
    font-family: 'VT323', monospace;
    cursor: pointer;
}

.send-button:hover {
    background: #cc00cc;
}

/* Success message */
.success-msg {
    text-align: center;
    padding: 15px;
    margin: 15px 0;
    border: 2px solid var(--cyber-purple);
    background: rgba(164,86,240,0.15);
    color: var(--cyber-purple);
    font-size: 22px;
    text-shadow: 0 0 8px rgba(164,86,240,.7);
    animation: pulse 2s infinite;
}

@keyframes pulse {
    from { opacity: 1; }
    to { opacity: 0.7; }
}

/* Character display */
.character-display {
    text-align: center;
    font-size: 20px;
    color: var(--cyber-purple);
    margin-bottom: 10px;
    text-transform: uppercase;
    text-shadow: 0 0 8px rgba(164,86,240,.6);
}

/* Treasure completion screen */
.treasure-screen {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.95);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    z-index: 2000;
    padding: 20px;
    overflow: hidden;
}

.treasure-box {
    font-size: 100px;
    margin-bottom: 20px;
    animation: bounce 2s infinite;
}

.congrats-text {
    font-size: 36px;
    color: gold;
    text-align: center;
    text-shadow: 0 0 10px gold, 0 0 20px orange;
    margin-bottom: 20px;
    animation: glow 1.5s infinite alternate;
}

@keyframes glow {
    from { text-shadow: 0 0 10px gold, 0 0 20px orange; }
    to { text-shadow: 0 0 20px gold, 0 0 30px orange, 0 0 40px yellow; }
}

.retro-text {
    font-size: 24px;
    color: var(--neon-green);
    text-align: center;
    margin-bottom: 30px;
    text-shadow: 0 0 5px var(--neon-green);
}

.restart-button {
    background: var(--magenta);
    color: #000;
    border: none;
    padding: 12px 24px;
    font-size: 20px;
    font-family: 'VT323', monospace;
    cursor: pointer;
    text-transform: uppercase;
}

.restart-button:hover {
    background: #cc00cc;
}

/* Balloon celebration */
.balloon {
    position: absolute;
    width: 40px;
    height: 50px;
    border-radius: 50%;
    animation: float 8s ease-in infinite;
    bottom: -100px;
}

.balloon:before {
    content: "";
    position: absolute;
    width: 2px;
    height: 30px;
    background: rgba(255, 255, 255, 0.5);
    bottom: -30px;
    left: 50%;
    transform: translateX(-50%);
}

@keyframes float {
    from {
        transform: translateY(0) rotate(0deg);
        opacity: 1;
    }
    to {
        transform: translateY(-100vh) rotate(20deg);
        opacity: 0;
    }
}

/* Scrollbar styling */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(0,0,0,0.2);
}

::-webkit-scrollbar-thumb {
    background: var(--cyber-purple);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #8a2be2;
}
</style>
"""

st.markdown(CRT_CSS, unsafe_allow_html=True)

# ---------- Init session state ----------
if "graph" not in st.session_state:
    st.session_state.graph = create_graph()
if "state" not in st.session_state:
    st.session_state.state: ChatState = {"messages": [], "character": "nami", "thread_id": "1"}
if "input_key" not in st.session_state:
    st.session_state.input_key = 0
if "success_message" not in st.session_state:
    st.session_state.success_message = None
if "show_success" not in st.session_state:
    st.session_state.show_success = False
if "treasure_found" not in st.session_state:
    st.session_state.treasure_found = False

# ---------- Celebration functions ----------
def create_balloons():
    balloon_html = ""
    colors = ["#ff0000", "#00ff00", "#0000ff", "#ffff00", "#ff00ff", "#00ffff", "#ffffff", "#ff9900"]
    for _ in range(30):
        color = random.choice(colors)
        left = random.randint(0, 100)
        delay = random.uniform(0, 5)
        duration = random.uniform(6, 10)
        balloon_html += f'<div class="balloon" style="left: {left}%; background-color: {color}; animation-delay: {delay}s; animation-duration: {duration}s;"></div>'
    return balloon_html

# ---------- Main app ----------
def main():
    # Show treasure completion screen if treasure found
    if st.session_state.treasure_found:
        # Create celebration elements
        balloons = create_balloons()
        
        st.markdown(
            f"""
            <div class="treasure-screen">
                {balloons}
                <div class="treasure-box">🎁</div>
                <div class="congrats-text">CONGRATULATIONS PIRATE!</div>
                <div class="retro-text">You've found the One Piece treasure!</div>
                <div class="retro-text">Boa Hancock has accepted your answer</div>
                <div class="retro-text">Your journey with the Straw Hats is complete</div>
                <div class="retro-text">Thanks for playing this retro treasure hunt!</div>
                <button class="restart-button" onclick="window.location.reload()">PLAY AGAIN</button>
            </div>
            """,
            unsafe_allow_html=True
        )
        return

    # Header with title and pirate flags
    st.markdown(
        """
        <div class="header">
            <h1 class="title">
                <span class="pirate-flag">🏴‍☠️</span>
                ONE PIECE TREASURE HUNT
                <span class="pirate-flag">🏴‍☠️</span>
            </h1>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Character display
    character_name = st.session_state.state["character"].upper()
    st.markdown(
        f'<div class="character-display">NOW TALKING WITH: {character_name}</div>',
        unsafe_allow_html=True
    )

    # Show success message if exists
    if st.session_state.show_success and st.session_state.success_message:
        st.markdown(f'<div class="success-msg">{st.session_state.success_message}</div>', unsafe_allow_html=True)
        # Clear success message after showing
        if st.session_state.get('clear_success', False):
            st.session_state.show_success = False
            st.session_state.success_message = None
        else:
            st.session_state.clear_success = True

    # Chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Render chat history
    for m in st.session_state.state["messages"]:
        if isinstance(m, AIMessage):
            # AI message on left
            st.markdown(
                f'<div class="message ai">'
                f'<div class="role">{st.session_state.state["character"].upper()}</div>'
                f'<div class="content">{m.content}</div>'
                f'</div>',
                unsafe_allow_html=True
            )
        else:
            # User message on right
            st.markdown(
                f'<div class="message user">'
                f'<div class="role">YOU</div>'
                f'<div class="content">{m.content}</div>'
                f'</div>',
                unsafe_allow_html=True
            )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Input container at bottom
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    
    # Use a form to handle input - Fixed the accessibility warning
    with st.form(key=f"input_form_{st.session_state.input_key}", clear_on_submit=True):
        col1, col2 = st.columns([6, 1])
        with col1:
            user_text = st.text_input(
                "Message input",  # Added a label for accessibility
                key=f"user_input_{st.session_state.input_key}", 
                placeholder="Type your message here...", 
                label_visibility="collapsed"  # Hide the label visually but keep it for accessibility
            )
        with col2:
            submitted = st.form_submit_button("SEND", use_container_width=True)
        
        if submitted and user_text:
            process_input(user_text)
    
    st.markdown('</div>', unsafe_allow_html=True)

def process_input(user_text):
    # Clear the input field by incrementing the key
    st.session_state.input_key += 1
    st.session_state.clear_success = False
    
    # Check if user solved current character's riddle
    new_state, success_message = check_riddle_solution(st.session_state.state, user_text)
    st.session_state.state = new_state
    
    # Check if the user has completed the treasure hunt (solved Boa's riddle)
    if st.session_state.state["character"] == "boa" and user_text.strip() == "28261879":
        st.session_state.treasure_found = True
        st.rerun()
    elif success_message:
        st.session_state.success_message = success_message
        st.session_state.show_success = True
        st.rerun()
    else:
        # Display user message
        st.session_state.state["messages"].append(HumanMessage(content=user_text))
        
        # Get AI response
        response = st.session_state.graph.invoke(
            {"messages": [HumanMessage(content=user_text)],
             "character": st.session_state.state["character"],
             "thread_id": st.session_state.state["thread_id"]},
            config={"configurable": {"thread_id": st.session_state.state["thread_id"], "node": "chat"}}
        )
        
        # Update state with the response
        st.session_state.state["messages"] = response.get("messages", [])
        
        # Rerun to update the UI
        st.rerun()

if __name__ == "__main__":
    main()