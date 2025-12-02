import streamlit as st
from chatbot_backend import workflow, HumanMessage
config={"configurable": {"thread_id": "1"}}
# session state -> 
if 'message_history' not in st.session_state :
    st.session_state['message_history'] = []


for message in st.session_state['message_history']:
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


