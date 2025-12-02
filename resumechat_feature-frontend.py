import streamlit as st
from chatbot_backend import workflow, HumanMessage
import uuid 


# Create a unique thread id
def create_unique_thread_id():
    thread_id = str(uuid.uuid4())
    return thread_id


def reset_chat():
    thread_id = create_unique_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    history = list(workflow.get_state_history({"configurable": {"thread_id": thread_id}}))
    messages = []
    for state in history:
        if "messages" in state:
            messages.extend(state["messages"])
    return messages

# session state -> 
if 'message_history' not in st.session_state :
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = create_unique_thread_id()

if "chat_threads" not in st.session_state:
    st.session_state['chat_threads'] = []


# Only add the thread if it's not already in the list

config = {"configurable": {"thread_id": st.session_state['thread_id']}}

#sidebar UI

st.sidebar.title("Welcome to the Chatbot")
if st.sidebar.button("New Chat"):
    st.session_state['thread_id'] = create_unique_thread_id()
    st.session_state['message_history'] = []
    add_thread(st.session_state['thread_id'])


st.sidebar.header("Conversation History")

selected_thread = st.session_state['thread_id']
for idx, thread_id in enumerate(st.session_state["chat_threads"]):
    if st.sidebar.button(str(thread_id), key=f"button_{thread_id}_{idx}"):
        selected_thread = thread_id


# Show all conversations from all threads, one after another
all_conversations = []
for thread_id in st.session_state["chat_threads"]:
    messages = load_conversation(thread_id)
    temp_messages = []
    for message in messages:
        if isinstance(message, HumanMessage):
            role = 'user'
        else:
            role = 'assistant'
        temp_messages.append({'role': role, 'content': message.content})
    all_conversations.append((thread_id, temp_messages))

for thread_id, messages in all_conversations:
    st.markdown(f"### Conversation Thread: {thread_id}")
    for message in messages:
        st.chat_message(message['role'])
        st.markdown(message['content'])




user_input = st.chat_input('Type here : ')


if user_input:

    
    
    st.session_state['message_history'].append({'role':'user' , 'content': user_input})

    with st.chat_message('user : '):
         st.text(user_input)
 
    

    with st.chat_message('assistant: '):
        ai_message = st.write_stream(message_chunk for message_chunk , metadata in workflow.stream(
        {'messages':[HumanMessage(content=user_input)]},
        config=config,
        stream_mode = "messages"
    ))

    st.session_state['message_history'].append({'role':'Assistant' , 'content': ai_message})
