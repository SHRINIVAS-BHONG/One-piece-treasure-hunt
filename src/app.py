from graph import create_graph
from state import ChatState
from utils import get_last_ai_message, check_riddle_solution
from langchain_core.messages import HumanMessage

def run_chatbot():
    chatbot = create_graph()
    state: ChatState = {"messages": [], "character": "nami", "thread_id": "1"}

    print("🔥 One Piece Treasure Hunt Chatbot 🔥")
    print("Start your journey! Type 'exit' to quit.\n")

    while True:
        user_message = input("You: ").strip()

        if user_message.lower() in ["exit", "quit", "bye"]:
            print(f"{state['character'].capitalize()}: Hmph, running away already? Fine, see you later~")
            break

        # First check if user solved current character's riddle
        state = check_riddle_solution(state, user_message)

        response = chatbot.invoke(
            {"messages": [HumanMessage(content=user_message)], "character": state["character"], "thread_id": state["thread_id"]},
            config={"configurable": {"thread_id": state["thread_id"], "node": "chat"}}
        )

        state["messages"] = response.get("messages", [])
        last_msg = get_last_ai_message(state["messages"])
        print(f"{state['character'].capitalize()}: {last_msg}")

if __name__ == "__main__":
    run_chatbot()