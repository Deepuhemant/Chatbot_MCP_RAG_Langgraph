from langgraph.graph import StateGraph, START, END, add_messages
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from dotenv import load_dotenv
# Prefer modern langchain import; fall back if not available
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
load_dotenv()

class ChatState(TypedDict):
    messages : Annotated[list[BaseMessage], add_messages]

llm = ChatOpenAI(model="gpt-4.1", temperature=0.7)

def chat(state: ChatState):
    messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages" : [response]}

checkpointer = MemorySaver()

graph = StateGraph(ChatState)

graph.add_node("chat_node", chat)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)
workflow = graph.compile(checkpointer=checkpointer)

