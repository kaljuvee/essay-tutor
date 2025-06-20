import streamlit as st
import asyncio
from agent.essay_tutor import EssayTutor, Message
import os

st.set_page_config(page_title="Essay Tutor Chat", page_icon="📝")
st.title("📝 Essay Tutor Chat")

# Initialize session state
if 'tutor' not in st.session_state:
    try:
        st.session_state['tutor'] = EssayTutor()
    except Exception as e:
        st.error(f"Error initializing EssayTutor: {e}")
        st.stop()
if 'session_id' not in st.session_state:
    st.session_state['session_id'] = 'web_session'
if 'history' not in st.session_state:
    st.session_state['history'] = []

# Helper to run async functions in Streamlit
def run_async(coro):
    return asyncio.run(coro)

# Chat input
with st.form(key='chat_form', clear_on_submit=True):
    user_input = st.text_input("You:", "", key="user_input")
    submit = st.form_submit_button("Send")

# Reset button
if st.button("Reset Session"):
    run_async(st.session_state['tutor'].reset_session(st.session_state['session_id']))
    st.session_state['history'] = []
    st.success("Session reset!")

# Handle user input
if submit and user_input.strip():
    # Add user message to history
    st.session_state['history'].append({
        'role': 'user',
        'content': user_input
    })
    # Get tutor response
    with st.spinner('Tutor is typing...'):
        try:
            response = run_async(
                st.session_state['tutor'].get_response(st.session_state['session_id'], user_input)
            )
        except Exception as e:
            st.error(f"Error: {e}")
            response = None
    if response:
        st.session_state['history'].append({
            'role': 'assistant',
            'content': response
        })

# Display chat history
for msg in st.session_state['history']:
    if msg['role'] == 'user':
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Tutor:** {msg['content']}")

st.caption("Essay Tutor powered by OpenAI and Streamlit.")
