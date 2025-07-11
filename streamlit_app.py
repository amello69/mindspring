# streamlit_app.py
import streamlit as st
from openai import OpenAI

# Secure API key
API_KEY = st.secrets["OPENAI"]["API_KEY"]

@st.cache_resource
def get_client():
    return OpenAI(api_key=API_KEY)

client = get_client()

st.set_page_config(page_title="English Tutor GPT‑4.1‑nano")
st.title("📝 English Tutor – GPT‑4.1‑nano")

# Initialize message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display conversation history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        
# ensure total_tokens is initialized
if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = 0
    
# Accept user input
if prompt := st.chat_input("Ask your English question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Call GPT-4.1-nano
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=st.session_state.messages,
            stream=False
        )
    except Exception as e:
        st.error(f"API call failed: {e}")
        raise
    reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)

    # Show token usage metrics
    # Safely extract usage only if available
ut = getattr(response, "usage", None)
if ut:
    prompt_toks = ut.get("prompt_tokens", 0)
    completion_toks = ut.get("completion_tokens", 0)
    total = prompt_toks + completion_toks
    st.session_state.total_tokens += total
    cost = st.session_state.total_tokens * (0.10 + 0.40) / 1_000_000

    st.sidebar.markdown(f"**Last session tokens:** {prompt_toks} in + {completion_toks} out = {total}")
    st.sidebar.markdown(f"**Total tokens so far:** {st.session_state.total_tokens}")
    st.sidebar.markdown(f"**Estimated cost:** ${cost:.4f}")
