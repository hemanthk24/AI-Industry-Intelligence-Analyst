import streamlit as st
from agent import run_agent

st.set_page_config(page_title="AI Analyst Agent", layout="wide")


# Sidebar (NEW)
with st.sidebar:
    st.title("⚙️ Settings")

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.write(
        "AI Industry Intelligence Agent that fetches real-time insights "
        "from research papers, GitHub, and web search."
    )

# -------------------------------
# Header
# -------------------------------
st.markdown(
    """
    <h1 style='text-align: center;'>🤖 AI Industry Intelligence Analyst</h1>
    <p style='text-align: center; color: gray;'>
    Real-time insights from research, GitHub & AI news
    </p>
    """,
    unsafe_allow_html=True
)

# -------------------------------
# Memory
# -------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------------
# Chat Display
# -------------------------------
chat_container = st.container()

with chat_container:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.markdown(msg["content"])
        else:
            with st.chat_message("assistant"):
                st.markdown(msg["content"])

# -------------------------------
# Input Box (Sticky bottom feel)
# -------------------------------
st.markdown("---")

user_input = st.chat_input("💬 Ask about AI trends, tools, research...")

if user_input:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    # -------------------------------
    # Agent Response
    # -------------------------------
    with st.chat_message("assistant"):
        with st.spinner("🤖 Thinking... fetching real-time insights..."):

            chat_history = st.session_state.messages[-10:]
            response = run_agent(user_input, chat_history)

            st.markdown(response)

    # Save response
    st.session_state.messages.append({"role": "assistant", "content": response})