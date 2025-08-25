from langchain_core.messages import AIMessage
from state import ChatState

def get_last_ai_message(messages):
    for msg in reversed(messages):
        if isinstance(msg, AIMessage) and msg.content.strip():
            return msg.content
    return "⚠️ No response."

def check_riddle_solution(state: ChatState, user_input: str):
    char = state["character"]
    success_message = None

    correct_answers = {
        "nami": ["26", "twenty-six"],
        "usopp": ["18"],
        "sanji": ["79"],
        "zoro": ["28"],
        "boa": ["28261879"]  # Fixed the answer
    }

    order = ["nami", "usopp", "sanji", "zoro", "boa"]

    if user_input.strip().lower() in [ans.lower() for ans in correct_answers[char]]:
        idx = order.index(char)
        if idx < len(order) - 1:
            next_char = order[idx + 1]
            success_message = f"✅ You solved {char.capitalize()}'s riddle! Moving to {next_char.capitalize()}..."
            state["character"] = next_char
            state["thread_id"] = str(idx + 2)
            state["messages"] = []  # reset for new character

    return state, success_message