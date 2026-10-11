import sqlite3
from pathlib import Path
from typing import Annotated, Sequence, TypedDict

from langchain_core.messages import BaseMessage, SystemMessage
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.prebuilt import ToolNode, tools_condition

from src.tools import save_flashcard
from src.database import DATA_DIR, init_db

# Initialize database schema on load
init_db()

# Local Qwen 2.5 14B instance
llm = ChatOllama(
    base_url="http://localhost:11434",
    model="qwen2.5:14b",
    temperature=0.3
)

tools = [save_flashcard]

class TutorState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    target_language: str

def tutor_node(state: TutorState):
    tutor_llm = llm.bind_tools(tools)
    target_lang = state.get("target_language", "Spanish")
    
    system_prompt = SystemMessage(
        content=(
            f"You are Syntext AI, an expert language tutor for {target_lang}.\n"
            f"1. Converse with the user in {target_lang}, providing English translations in brackets where helpful.\n"
            f"2. Gently correct any grammar mistakes at the very beginning of your response.\n"
            f"3. Whenever introducing key vocabulary or idioms, invoke the `save_flashcard` tool to store them. DO NOT ask for permission, just save it automatically and tell the user you saved it."
        )
    )
    
    response = tutor_llm.invoke([system_prompt] + list(state["messages"]))
    return {"messages": [response]}

# Build Graph
workflow = StateGraph(TutorState)

# Add nodes
workflow.add_node("tutor", tutor_node)
workflow.add_node("tools", ToolNode(tools)) # This physically runs the Python function

# Add edges
workflow.add_edge(START, "tutor")

# If the tutor decides to use a tool, go to "tools". Otherwise, end the turn.
workflow.add_conditional_edges("tutor", tools_condition)

# After the tool runs, go back to the tutor so it can read the success message and reply
workflow.add_edge("tools", "tutor")

# SQLite Memory Checkpointer
memory_db_path = DATA_DIR / "syntext_memory.db"
conn = sqlite3.connect(memory_db_path, check_same_thread=False)
memory = SqliteSaver(conn)

syntext_app = workflow.compile(checkpointer=memory)