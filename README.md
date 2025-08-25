# 🌊🎩 **Retro Waves with StrawHats**  

*A conversational cyber-adventure through the world of **One Piece** where you solve riddles to uncover **Luffy’s hidden treasure***  

---

## 🏴‍☠️ **Overview**  
This project is an **interactive chatbot game** where you chat with **five iconic One Piece characters**, each staying true to their anime personality.  
Your mission: **solve riddles** given by each Straw Hat ally (and rival) to progress on the journey toward Luffy’s treasure.  

---

## 👥 **Characters**  

- 🧭 **Nami (The Navigator)** – Money-obsessed, demands payment before helping  
- 🎯 **Usopp (The Sniper)** – Boastful storyteller full of tall tales  
- 👨‍🍳 **Sanji (The Chef)** – Flirtatious, poetic, and charming  
- ⚔️ **Zoro (The Swordsman)** – Stoic, direct, and intimidating  
- 👑 **Boa Hancock (The Pirate Empress)** – Regal, prideful, demands admiration  

---

## 💻 **Tech Stack**  

- **Core Frameworks**: [LangGraph](https://www.langchain.com/langgraph), [LangChain](https://www.langchain.com/)  
- **Frontend / UI**: [Streamlit](https://streamlit.io/) (retro cyberpunk styling)  
- **Language**: [Python](https://www.python.org/)  
- **LLM Provider**: [Groq API](https://groq.com/)  

---

## 🎮 **How It Works**  

### 🔹 **Character Personalities & Behaviors**  
Each character interacts authentically, reflecting their quirks from the anime.  
They chat casually on any topic but **only reveal riddles** when asked about:  
`"Luffy’s treasure"` or `"secrets"`  

### 🔹 **Game Progression**  
1. Start with **Nami**  
2. Ask about `"Luffy’s treasure"` → Receive her riddle  
3. Solve it to unlock the next character  
4. Repeat until **Boa Hancock**  
5. Solve her **master riddle** to claim the treasure!  

### 🔹 **Free Conversation**  
- Chat casually for fun 😄  
- Riddles are **guarded secrets** — only revealed when triggered  
- Each solved riddle brings you closer to the **ultimate prize**  

---

## 🧩 **Riddles & Solutions**  

- 🧭 **Nami**:  
  `"The answer lies in the alphabet of any navigator..."`  
  ➝ **Answer: 26**  

- 🎯 **Usopp**:  
  `"Two crews of nine men..."`  
  ➝ **Answer: 18**  

- 👨‍🍳 **Sanji**:  
  `"Seven ladies gave their hearts..."`  
  ➝ **Answer: 79**  

- ⚔️ **Zoro**:  
  `"Four cardinal winds guide the path..."`  
  ➝ **Answer: 28**  

- 👑 **Boa Hancock**:  
  `"Answer is in past, not present or future..."`  
  ➝ **Answer: 28261879**  

---

## ⚙️ **Setup Instructions**  

### 📋 **Prerequisites**  
- Python **3.8+**  
- **Groq API key** (for LLM responses)  

### 📥 **Installation**  
```bash
git clone <your-repo-url>
cd retro-waves-strawhats
pip install langchain-core langchain-groq langgraph python-dotenv streamlit
```

### 🔑 **Environment Setup**  
Create a `.env` file:  
```text
GROQ_API_KEY=your_api_key_here
```  

---

## 🚀 **Running the Application**  

### 🔹 Command Line Interface (CLI)  
```bash
python app.py
```

### 🔹 Web Interface (Recommended)  
```bash
streamlit run streamlit_app.py
```  

✨ The web app has a **retro cyberpunk CRT-style theme** with scanlines & glowing effects for immersion.  

---

## 📂 **Project Structure**  
```
retro-waves-strawhats/
│── app.py              # CLI chatbot
│── streamlit_app.py    # Web interface with retro visuals
│── character.py        # Personalities & riddles
│── config.py           # Config & Groq API setup
│── graph.py            # Conversation flow (LangGraph)
│── state.py            # Conversation state management
│── utils.py            # Helper functions (riddle checks, etc.)
│── .env                # API key (not committed)
```

---

## 🕹️ **How to Play**  
1. Start chatting with **Nami**  
2. Ask about `"Luffy’s treasure"` or `"secrets"`  
3. Solve riddles to progress  
4. Unlock all characters and **reach the ultimate treasure**  

---

## ✨ **Features**  

- 🎭 Authentic **One Piece character personalities**  
- 🔑 Progressive **riddle challenges**  
- 🌐 **CLI & Web interface** options  
- 🖥️ **Retro cyberpunk visuals** in web mode  
- 🎉 Celebration animation upon treasure completion  
- 💾 Persistent conversation state  

---

## 🏆 **Tips for Playing**  

- 💬 Take time for **fun casual chats** before treasure hunting  
- 🧠 Riddles may require **logic, numbers, or One Piece knowledge**  
- 🔍 Characters’ personalities give subtle hints  
- 🎩 Stay sharp — the treasure is waiting!  

---

**Youtube link** = [link](https://youtu.be/NwrHbWzcxGI)

🌊 **Set sail, pirate!** 🏴‍☠️  
