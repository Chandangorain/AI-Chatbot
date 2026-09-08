# -> create new frontend and backend files
#
# -> install https://pypi.org/project/langgraph-checkpoint-sqlite/
#
# -> implement database in backend
#
# -> chat in multiple threads
#
# -> install and visualize
#
# -> integrate to frontend






from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import sqlite3

load_dotenv()

llm = ChatOpenAI()

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    messages = state['messages']
    response = llm.invoke(messages)
    return {"messages": [response]}

## sqlite3 connection
conn = sqlite3.connect(database='chatbot.db', check_same_thread=False)

# Checkpointer
checkpointer = SqliteSaver()

graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)