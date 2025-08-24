from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage
from character import character_prompts
from config import get_llm
from state import ChatState

def create_graph():
    llm = get_llm()
    
    # Create prompt templates
    chat_templates = {
        char: ChatPromptTemplate.from_messages([
            ("system", prompt),
            MessagesPlaceholder(variable_name="current_chat_history")
        ])
        for char, prompt in character_prompts.items()
    }

    # Response function
    def chat_response(state: ChatState):
        char = state["character"]
        template = chat_templates[char]
        prompt = template.invoke({"current_chat_history": state["messages"]})
        response = llm.invoke(prompt.to_messages())

        if isinstance(response, AIMessage) and response.content.strip():
            state["messages"].append(response)

        return {"messages": state["messages"], "character": state["character"], "thread_id": state["thread_id"]}

    # Build graph
    checkpointer = MemorySaver()
    graph = StateGraph(ChatState)
    graph.add_node("chat", chat_response)
    graph.add_edge(START, "chat")
    graph.add_edge("chat", END)
    
    return graph.compile(checkpointer=checkpointer)