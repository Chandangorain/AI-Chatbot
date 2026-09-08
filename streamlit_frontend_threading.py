# this is for resume chat features for the chatbot

# -> add a sidebar with title + A Start Chat Button + A title named 'My Conversations'
# 
# -> generate dynamic thread Id and add it to the session
# 
# -> Display the thread id in sidebar
# 
# ********************************************************************************
# 
# -> add a New Chat button
# 
# -> On Click of new chat open a new chat window
#     * generate a new thread_id
#     * save it in session
#     * reset message history
# 
# ********************************************************************************
# 
# -> create a list to store all thread_ids
# 
# -> Load all the thread ids in the sidebar
# 
# -> convert the side bar text to clickable buttons
# 
# ********************************************************************************
# 
# -> on click of a particular thread id load that particular conversation


import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage

##################################### session setup #####################################

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

########################## sidebar ui #####################################
st.sidebar.title('LangGraph Chatbot')
st.sidebar.button('Start New Chat')

st.sidebar.header('My Conversations')

################################ Main UI #####################################
# loading the conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

#{'role': 'user', 'content': 'Hi'}
#{'role': 'assistant', 'content': 'Hi=ello'}

user_input = st.chat_input('Type here')

if user_input:

    # first add the message to message_history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    # first add the message to message_history
    with st.chat_message('assistant'):

# we are getting message_chunk, metadata from chatbot.stream()
#then we are sending content of the message_chunk to st.write_stream() which will display the content 
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config= {'configurable': {'thread_id': 'thread-1'}},
                stream_mode= 'messages'
            )
        )
        

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})