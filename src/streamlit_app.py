# streamlit_app.py
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from graph import create_graph
from state import ChatState
from utils import check_riddle_solution
import random

# ---------- Page config ----------
st.set_page_config(
    page_title="Retro waves with Strawhats",
    page_icon="⚡",  
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- Enhanced Retro Cyberpunk CSS with CRT Effects ----------
RETRO_CYBERPUNK_CSS = """
<style>
/* Import retro-style fonts */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap');

:root {
  --neon-cyan: #00ffff;
  --neon-pink: #ff007f;
  --neon-green: #39ff14;
  --electric-blue: #0080ff;
  --cyber-purple: #8a2be2;
  --warning-orange: #ff8800;
  --matrix-green: #00ff00;
  --dark-bg: #0a0a0a;
  --terminal-bg: #1a1a2e;
  --card-bg: rgba(26, 26, 46, 0.8);
}

/* Global reset and base styles */
html, body, [class*="block-container"] {
  background: var(--dark-bg) !important;
  padding: 0 !important;
  margin: 0 !important;
  overflow-x: hidden;
}

* {
  font-family: 'Share Tech Mono', monospace !important;
  letter-spacing: 0.5px;
}

/* Hide Streamlit default elements */
header[data-testid="stHeader"], 
footer,
.stChatInputContainer,
.stDeployButton,
div[data-testid="stDecoration"] {
  visibility: hidden !important;
  height: 0 !important;
  display: none !important;
}

/* Main container with animated grid background */
.main {
  position: relative;
  padding: 0 !important;
  margin: 0 !important;
  min-height: 100vh;
  background: 
    linear-gradient(rgba(0, 255, 255, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 255, 255, 0.03) 1px, transparent 1px);
  background-size: 50px 50px;
  animation: gridMove 20s linear infinite;
}

@keyframes gridMove {
  0% { background-position: 0 0, 0 0; }
  100% { background-position: 50px 50px, 50px 50px; }
}

/* Enhanced CRT effects */
.main::before {
  content: "";
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: 
    repeating-linear-gradient(
      0deg,
      rgba(0, 0, 0, 0.2),
      rgba(0, 0, 0, 0.2) 1px,
      transparent 1px,
      transparent 3px
    );
  pointer-events: none;
  z-index: 1000;
  animation: scanlines 0.1s linear infinite;
}

@keyframes scanlines {
  0% { transform: translateY(0); }
  100% { transform: translateY(3px); }
}

/* CRT screen curvature effect */
.main::after {
  content: "";
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(
    ellipse at center,
    transparent 60%,
    rgba(0, 0, 0, 0.3) 100%
  );
  pointer-events: none;
  z-index: 999;
}

/* Glitch animations */
@keyframes glitch {
  0%, 100% { transform: translate(0); }
  10% { transform: translate(-2px, 2px); }
  20% { transform: translate(-2px, -2px); }
  30% { transform: translate(2px, 2px); }
  40% { transform: translate(2px, -2px); }
  50% { transform: translate(-1px, 2px); }
  60% { transform: translate(-1px, -2px); }
  70% { transform: translate(1px, 1px); }
  80% { transform: translate(-1px, -1px); }
  90% { transform: translate(1px, 2px); }
}

@keyframes textGlow {
  0%, 100% { 
    text-shadow: 
      0 0 5px currentColor,
      0 0 10px currentColor,
      0 0 15px currentColor;
  }
  50% { 
    text-shadow: 
      0 0 10px currentColor,
      0 0 20px currentColor,
      0 0 30px currentColor;
  }
}

/* Enhanced header */
.cyber-header {
  text-align: center;
  padding: 20px 0;
  margin-bottom: 20px;
  background: linear-gradient(45deg, var(--terminal-bg), transparent);
  border-bottom: 2px solid var(--neon-cyan);
  border-image: linear-gradient(90deg, var(--neon-cyan), var(--neon-pink), var(--neon-cyan)) 1;
  position: relative;
}

.cyber-header::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, 
    transparent, 
    var(--neon-cyan) 20%, 
    var(--neon-pink) 50%, 
    var(--neon-cyan) 80%, 
    transparent
  );
  animation: borderFlow 3s ease-in-out infinite;
}

@keyframes borderFlow {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 1; }
}

.cyber-title {
  font-family: 'Orbitron', monospace !important;
  font-size: 48px;
  font-weight: 900;
  text-transform: uppercase;
  background: linear-gradient(45deg, var(--neon-cyan), var(--neon-pink), var(--electric-blue));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: textGlow 2s ease-in-out infinite, glitch 5s infinite;
  margin: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
}

.cyber-icon {
  font-size: 42px;
  color: var(--neon-pink);
  animation: pulse 2s infinite, rotate 10s linear infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.1); opacity: 0.8; }
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Character display enhancement */
.character-terminal {
  text-align: center;
  font-size: 24px;
  color: var(--matrix-green);
  margin: 20px 0;
  padding: 10px 20px;
  background: rgba(0, 255, 0, 0.1);
  border: 1px solid var(--matrix-green);
  border-radius: 5px;
  text-transform: uppercase;
  animation: textGlow 1.5s ease-in-out infinite;
  position: relative;
}

.character-terminal::before {
  content: ">>> NEURAL LINK ESTABLISHED <<<";
  position: absolute;
  top: -15px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 12px;
  color: var(--neon-cyan);
  background: var(--dark-bg);
  padding: 0 10px;
}

/* Enhanced chat container */
.cyber-chat-container {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  margin-bottom: 100px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  max-height: calc(100vh - 300px);
}

/* Enhanced message styling */
.cyber-message {
  max-width: 75%;
  padding: 15px 20px;
  border-radius: 0;
  position: relative;
  backdrop-filter: blur(10px);
  animation: messageAppear 0.5s ease-out;
}

@keyframes messageAppear {
  from { 
    opacity: 0; 
    transform: translateY(20px); 
  }
  to { 
    opacity: 1; 
    transform: translateY(0); 
  }
}

.cyber-message::before {
  content: "";
  position: absolute;
  top: 0;
  bottom: 0;
  width: 3px;
  animation: energyPulse 2s ease-in-out infinite;
}

@keyframes energyPulse {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 1; }
}

.cyber-message.ai {
  align-self: flex-start;
  background: linear-gradient(135deg, rgba(57, 255, 20, 0.15), rgba(0, 255, 255, 0.1));
  border: 1px solid var(--neon-green);
  border-left: 4px solid var(--neon-green);
  margin-right: auto;
}

.cyber-message.ai::before {
  left: 0;
  background: linear-gradient(180deg, var(--neon-green), var(--neon-cyan));
}

.cyber-message.user {
  align-self: flex-end;
  background: linear-gradient(135deg, rgba(255, 0, 127, 0.15), rgba(128, 0, 255, 0.1));
  border: 1px solid var(--neon-pink);
  border-right: 4px solid var(--neon-pink);
  margin-left: auto;
}

.cyber-message.user::before {
  right: 0;
  background: linear-gradient(180deg, var(--neon-pink), var(--cyber-purple));
}

.message-role {
  font-size: 14px;
  font-weight: bold;
  opacity: 0.9;
  margin-bottom: 8px;
  text-transform: uppercase;
  font-family: 'Orbitron', monospace !important;
}

.message-content {
  font-size: 18px;
  line-height: 1.4;
  white-space: pre-wrap;
}

.cyber-message.ai .message-content {
  color: var(--neon-green);
  text-shadow: 0 0 8px rgba(57, 255, 20, 0.6);
}

.cyber-message.user .message-content {
  color: var(--neon-pink);
  text-shadow: 0 0 8px rgba(255, 0, 127, 0.6);
}

.cyber-message.ai .message-role {
  color: var(--neon-cyan);
}

.cyber-message.user .message-role {
  color: var(--electric-blue);
}

/* Enhanced input terminal */
.cyber-input-terminal {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 20px;
  background: linear-gradient(180deg, transparent, var(--terminal-bg));
  border-top: 2px solid var(--neon-pink);
  backdrop-filter: blur(20px);
  z-index: 1001;
}

.cyber-input-terminal::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, 
    var(--neon-pink), 
    var(--neon-cyan), 
    var(--neon-pink)
  );
  animation: terminalPulse 2s ease-in-out infinite;
}

@keyframes terminalPulse {
  0%, 100% { opacity: 0.7; }
  50% { opacity: 1; }
}

/* Form styling */
div[data-testid="stForm"] {
  background: transparent !important;
  border: none !important;
}

/* Input field styling */
input[type="text"] {
  background: rgba(0, 0, 0, 0.7) !important;
  border: 2px solid var(--neon-cyan) !important;
  color: var(--neon-cyan) !important;
  padding: 15px !important;
  font-size: 18px !important;
  font-family: 'Share Tech Mono', monospace !important;
  border-radius: 0 !important;
  box-shadow: inset 0 0 20px rgba(0, 255, 255, 0.1) !important;
}

input[type="text"]:focus {
  outline: none !important;
  border-color: var(--neon-pink) !important;
  box-shadow: 
    inset 0 0 20px rgba(255, 0, 127, 0.1),
    0 0 20px rgba(255, 0, 127, 0.3) !important;
  color: var(--neon-pink) !important;
}

input[type="text"]::placeholder {
  color: rgba(0, 255, 255, 0.5) !important;
}

/* Button styling */
button[kind="primary"] {
  background: linear-gradient(45deg, var(--neon-pink), var(--cyber-purple)) !important;
  color: #000 !important;
  border: none !important;
  padding: 15px 25px !important;
  font-size: 16px !important;
  font-family: 'Orbitron', monospace !important;
  font-weight: bold !important;
  text-transform: uppercase !important;
  cursor: pointer !important;
  border-radius: 0 !important;
  box-shadow: 0 0 20px rgba(255, 0, 127, 0.3) !important;
  transition: all 0.3s ease !important;
}

button[kind="primary"]:hover {
  background: linear-gradient(45deg, var(--cyber-purple), var(--neon-pink)) !important;
  box-shadow: 0 0 30px rgba(255, 0, 127, 0.5) !important;
  transform: translateY(-2px) !important;
}

/* Success message styling */
.cyber-success {
  text-align: center;
  padding: 20px;
  margin: 20px 0;
  background: linear-gradient(45deg, rgba(138, 43, 226, 0.2), rgba(255, 136, 0, 0.1));
  border: 2px solid var(--warning-orange);
  color: var(--warning-orange);
  font-size: 24px;
  font-weight: bold;
  text-transform: uppercase;
  animation: successPulse 1s ease-in-out infinite, glitch 3s infinite;
  position: relative;
  overflow: hidden;
}

.cyber-success::before {
  content: "";
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, 
    transparent, 
    rgba(255, 136, 0, 0.3), 
    transparent
  );
  animation: successSweep 2s ease-in-out infinite;
}

@keyframes successPulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.02); }
}

@keyframes successSweep {
  0% { left: -100%; }
  100% { left: 100%; }
}

/* Treasure screen enhancement */
.cyber-treasure-screen {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at center, var(--dark-bg) 0%, #000 100%),
    repeating-linear-gradient(
      45deg,
      transparent,
      transparent 2px,
      rgba(0, 255, 255, 0.03) 2px,
      rgba(0, 255, 255, 0.03) 4px
    );
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 2000;
  padding: 20px;
  overflow: hidden;
  animation: screenFlicker 0.1s infinite;
}

@keyframes screenFlicker {
  0%, 98%, 100% { opacity: 1; }
  99% { opacity: 0.98; }
}

.treasure-icon {
  font-size: 120px;
  margin-bottom: 30px;
  animation: treasureBounce 2s ease-in-out infinite;
  filter: drop-shadow(0 0 20px gold);
}

@keyframes treasureBounce {
  0%, 100% { transform: translateY(0) scale(1); }
  50% { transform: translateY(-20px) scale(1.1); }
}

.cyber-congrats {
  font-family: 'Orbitron', monospace !important;
  font-size: 42px;
  font-weight: 900;
  background: linear-gradient(45deg, gold, orange, yellow, gold);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-align: center;
  margin-bottom: 20px;
  animation: congratsGlow 2s ease-in-out infinite, glitch 4s infinite;
}

@keyframes congratsGlow {
  0%, 100% { 
    filter: drop-shadow(0 0 10px gold) drop-shadow(0 0 20px orange);
  }
  50% { 
    filter: drop-shadow(0 0 20px gold) drop-shadow(0 0 40px orange) drop-shadow(0 0 60px yellow);
  }
}

.cyber-treasure-text {
  font-size: 22px;
  color: var(--neon-green);
  text-align: center;
  margin-bottom: 15px;
  animation: textGlow 2s ease-in-out infinite;
}

.cyber-restart-button {
  background: linear-gradient(45deg, var(--neon-pink), var(--cyber-purple)) !important;
  color: #000 !important;
  border: none !important;
  padding: 15px 30px !important;
  font-size: 20px !important;
  font-family: 'Orbitron', monospace !important;
  font-weight: bold !important;
  cursor: pointer !important;
  text-transform: uppercase !important;
  border-radius: 0 !important;
  animation: buttonGlow 1.5s ease-in-out infinite !important;
  box-shadow: 0 0 30px rgba(255, 0, 127, 0.5) !important;
}

@keyframes buttonGlow {
  0%, 100% { 
    box-shadow: 0 0 30px rgba(255, 0, 127, 0.5);
    transform: scale(1);
  }
  50% { 
    box-shadow: 0 0 40px rgba(255, 0, 127, 0.8);
    transform: scale(1.05);
  }
}


@keyframes particleFloat {
  from {
    transform: translateY(100vh) translateX(0) rotate(0deg);
    opacity: 0;
  }
  10% { opacity: 1; }
  90% { opacity: 1; }
  to {
    transform: translateY(-20vh) translateX(100px) rotate(360deg);
    opacity: 0;
  }
}

/* Scrollbar enhancement */
::-webkit-scrollbar {
  width: 12px;
}

::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(0, 255, 255, 0.1);
}

::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, var(--neon-cyan), var(--neon-pink));
  border-radius: 0;
  box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.5);
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, var(--neon-pink), var(--cyber-purple));
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .cyber-title {
    font-size: 32px;
    flex-direction: column;
    gap: 10px;
  }
  
  .cyber-message {
    max-width: 90%;
  }
  
  .message-content {
    font-size: 16px;
  }
}
</style>
"""

st.markdown(RETRO_CYBERPUNK_CSS, unsafe_allow_html=True)

# ---------- Init session state ----------
@st.cache_resource
def initialize_graph():
    """Initialize the graph with caching to prevent threading issues"""
    try:
        return create_graph()
    except Exception as e:
        st.error(f"⚡ Failed to initialize neural network: {e}")
        return None

if "graph" not in st.session_state:
    st.session_state.graph = initialize_graph()
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
if "app_ready" not in st.session_state:
    st.session_state.app_ready = st.session_state.graph is not None

# ---------- Main app ----------
def main():
    # Check if app is ready
    if not st.session_state.get('app_ready', False):
        st.markdown(
            """
            <div style="text-align: center; padding: 50px; color: var(--neon-cyan);">
                <h2>⚡ INITIALIZING CYBERPUNK TERMINAL ⚡</h2>
                <p>Neural networks loading...</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.rerun()
        return

    
    # Show enhanced treasure completion screen
    if st.session_state.treasure_found:        
        st.markdown(
            f"""
            <div class="cyber-treasure-screen">
                <div class="treasure-icon">💎</div>
               <div class="cyber-congrats">🎉 YOU'VE CLAIMED LUFFY'S TREASURE! 🎉</div>
               <div class="cyber-treasure-text">◆ STRAW HAT LEGACY UNLOCKED ◆</div>
               <div class="cyber-treasure-text">◆ PIRATE KING'S PATHWAY DISCOVERED ◆</div>
               <div class="cyber-treasure-text">◆ GRAND LINE ODYSSEY COMPLETED ◆</div>
               <div class="cyber-treasure-text">◆ TREASURE HUNT SESSION TERMINATED ◆</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        return

    # Enhanced header with cyberpunk styling
    st.markdown(
        """
        <div class="cyber-header">
            <h1 class="cyber-title">
                <span class="cyber-icon">⚡</span>
                 Retro waves with Strawhats
                <span class="cyber-icon">⚡</span>
            </h1>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Enhanced character display
    character_name = st.session_state.state["character"].upper()
    st.markdown(
        f'''
        <div class="character-terminal">
            ACTIVE CONNECTION: {character_name}
        </div>
        ''',
        unsafe_allow_html=True
    )

    # Show enhanced success message
    if st.session_state.show_success and st.session_state.success_message:
        st.markdown(
            f'<div class="cyber-success">⚡ {st.session_state.success_message} ⚡</div>', 
            unsafe_allow_html=True
        )
        if st.session_state.get('clear_success', False):
            st.session_state.show_success = False
            st.session_state.success_message = None
        else:
            st.session_state.clear_success = True

    # Enhanced chat container
    st.markdown('<div class="cyber-chat-container">', unsafe_allow_html=True)
    
    # Render chat history with enhanced styling
    for m in st.session_state.state["messages"]:
        if isinstance(m, AIMessage):
            # Enhanced AI message
            st.markdown(
                f'''
                <div class="cyber-message ai">
                    <div class="message-role">◆ {st.session_state.state["character"].upper()} ◆</div>
                    <div class="message-content">{m.content}</div>
                </div>
                ''',
                unsafe_allow_html=True
            )
        else:
            # Enhanced user message
            st.markdown(
                f'''
                <div class="cyber-message user">
                    <div class="message-role">◆ USER.TERMINAL ◆</div>
                    <div class="message-content">{m.content}</div>
                </div>
                ''',
                unsafe_allow_html=True
            )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Enhanced input terminal
    st.markdown('<div class="cyber-input-terminal">', unsafe_allow_html=True)
    
    # Enhanced form with cyberpunk styling
    with st.form(key=f"cyber_input_form_{st.session_state.input_key}", clear_on_submit=True):
        col1, col2 = st.columns([5, 1])
        with col1:
            user_text = st.text_input(
                "Terminal Input",
                key=f"cyber_user_input_{st.session_state.input_key}", 
                placeholder=">>> Enter command...", 
                label_visibility="collapsed"
            )
        with col2:
            submitted = st.form_submit_button("⚡ EXECUTE", use_container_width=True)
        
        if submitted and user_text:
            process_input(user_text)
    
    st.markdown('</div>', unsafe_allow_html=True)

def process_input(user_text):
    # Clear the input field by incrementing the key
    st.session_state.input_key += 1
    st.session_state.clear_success = False
    
    try:
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
            
            # Get AI response with error handling
            try:
                if st.session_state.graph is None:
                    raise Exception("Neural network not initialized")
                    
                response = st.session_state.graph.invoke(
                    {"messages": [HumanMessage(content=user_text)],
                     "character": st.session_state.state["character"],
                     "thread_id": st.session_state.state["thread_id"]},
                    config={"configurable": {"thread_id": st.session_state.state["thread_id"], "node": "chat"}}
                )
                
                # Update state with the response
                st.session_state.state["messages"] = response.get("messages", [])
                
            except RuntimeError as e:
                error_msg = str(e).lower()
                if "cannot schedule new futures after shutdown" in error_msg or "executor" in error_msg:
                    # Handle the executor shutdown gracefully
                    st.error("⚡ SYSTEM ERROR: Neural link disrupted. Reinitializing...")
                    st.session_state.graph = initialize_graph()
                    st.session_state.app_ready = st.session_state.graph is not None
                    st.session_state.state["messages"].append(
                        AIMessage(content="🔴 SYSTEM REBOOT: Connection restored. Please try your command again.")
                    )
                else:
                    raise e
            except Exception as e:
                st.error(f"⚡ TERMINAL ERROR: {str(e)}")
                st.session_state.state["messages"].append(
                    AIMessage(content=f"🔴 ERROR: {str(e)}")
                )
            
            # Rerun to update the UI
            st.rerun()
            
    except Exception as e:
        st.error(f"⚡ CRITICAL SYSTEM ERROR: {str(e)}")
        st.stop()

if __name__ == "__main__":
    main()