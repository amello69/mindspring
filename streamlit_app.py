# streamlit_app.py
import streamlit as st
from openai import OpenAI

# Securely load API key
API_KEY = st.secrets["OPENAI"]["API_KEY"]

@st.cache_resource
def get_client():
    return OpenAI(api_key=API_KEY)

client = get_client()

st.set_page_config(page_title="English Tutor (GPT‑4.1‑nano)")
st.title("📝 English Tutor – GPT‑4.1‑nano")

# Initialize session message history & total tokens
if "messages" not in st.session_state:
    st.session_state.messages = []
if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = 0

# Render chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Handle new user input
if prompt := st.chat_input("Ask your English question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Call GPT‑4.1‑nano and capture errors
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=st.session_state.messages,
            stream=False,
        )
    except Exception as e:
        st.error(f"❌ API call failed:\n```\n{e}\n```")
        st.stop()

    reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)

    # Safe token usage tracking
    if hasattr(response, "usage") and response.usage:
        prompt_toks = getattr(response.usage, "prompt_tokens", 0)
        completion_toks = getattr(response.usage, "completion_tokens", 0)
        session_toks = prompt_toks + completion_toks

        st.session_state.total_tokens += session_toks
        estimated_cost = st.session_state.total_tokens * (0.10 + 0.40) / 1_000_000

        st.sidebar.markdown(f"**Last session tokens:** {prompt_toks} in, {completion_toks} out = {session_toks}")
        st.sidebar.markdown(f"**Total tokens so far:** {st.session_state.total_tokens}")
        st.sidebar.markdown(f"**Estimated cost:** ${estimated_cost:.4f}")
    else:
        st.sidebar.markdown("⚠️ Token usage data not available for this request.")
