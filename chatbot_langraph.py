#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from langgraph.graph import StateGraph, START, END, add_messages
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from dotenv import load_dotenv
# Prefer modern langchain import; fall back if not available
try:
    from langchain.chat_models import ChatOpenAI
except Exception:
    try:
        from langchain_openai import ChatOpenAI
    except Exception:
        ChatOpenAI = None
load_dotenv()


# In[6]:


class ChatState(TypedDict):
    messages : Annotated[list[BaseMessage], add_messages]


# In[7]:


llm = ChatOpenAI(model="gpt-4.1", temperature=0.7)


# In[ ]:


graph = StateGraph(ChatState)


# In[ ]:


grph

