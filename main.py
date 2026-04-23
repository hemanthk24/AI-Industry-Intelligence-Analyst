import streamlit as st
from agent import run_agent

st.set_page_config(page_title="AI Analyst Agent", layout="wide")

# Centered Title
st.markdown(
    """
    <h1 style='text-align: center;'>🤖 AI Industry Intelligence Analyst</h1>
    <p style='text-align: center;'>Ask anything about latest AI trends, tools, and research</p>
    """,
    unsafe_allow_html=True
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Ask about AI trends, tools, research...")

if user_input:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    # Run agent
    with st.spinner("Thinking..."):
        response = run_agent(user_input)

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):
        st.markdown(response)

# Clear chat button (optional but useful)
if st.button("Clear Chat"):
    st.session_state.messages = []