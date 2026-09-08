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
# -> convert the side bar text to clickable buttons    ->button
# 
# ********************************************************************************
# 
# -> on click of a particular thread id load that particular conversation


import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage
import uuid


########################  utility functions #####################################
def generate_thread_id():   # random thread_id generation
    thread_id=uuid.uuid4()
    return thread_id


def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

# this functions helps to return the conversation history for a psrticular thread when the thread id is clicked in my conversations
def load_conversation(thread_id):
    state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}})
    # Check if messages key exists in state values, return empty list if not
    return state.values.get('messages', [])

##################################### session setup #####################################

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()


if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()


if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = []

add_thread(st.session_state['thread_id'])

########################## sidebar ui #####################################
st.sidebar.title('LangGraph Chatbot')
if st.sidebar.button('New Chat'):
    reset_chat()        # new chat clicked -> call reset chat()

st.sidebar.header('My Conversations')

for thread_id in st.session_state['chat_threads'][::-1]:  # this stores the thread id in a list . 
    if st.sidebar.button(str(thread_id)):           # if thread_id clicked
        st.session_state['thread_id'] = thread_id   #then update the thread_id
        messages = load_conversation(thread_id)     # and retrieve the conversation history by calling load_conversation() function



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


    CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}

    # first add the message to message_history
    with st.chat_message('assistant'):

# we are getting message_chunk, metadata from chatbot.stream()
#then we are sending content of the message_chunk to st.write_stream() which will display the content 
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                 config=CONFIG,
                stream_mode= 'messages'
            )
        )
        

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})