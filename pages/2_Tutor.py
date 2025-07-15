import streamlit as st
from openai import OpenAI

# Securely get API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI"]["API_KEY"])

# --- Auth check ---
if "logged_in_user" not in st.session_state:
    st.warning("Please log in from the main page.")
    st.stop()

# --- Init chat history & input box ---
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if "my_input_box" not in st.session_state:
    st.session_state["my_input_box"] = ""

# --- Tutor page UI ---
st.title("🗣️ AI English Tutor")

username = st.session_state.get("logged_in_user", "")
name = st.session_state.get("logged_in_name", "")
tokens_remaining = st.session_state.get("tokens_remaining", 0)

st.sidebar.markdown(f"**Tokens remaining:** {tokens_remaining}")

if tokens_remaining <= 0:
    st.error("You have exhausted your monthly tokens. Please purchase more.")
    st.stop()

# --- Clear chat button ---
if st.button("🗑️ Clear Chat"):
    st.session_state["chat_history"] = []
    st.success("Chat history cleared!")
    st.experimental_rerun()

# --- Display chat history ---
for chat in st.session_state["chat_history"]:
    if chat["role"] == "user":
        st.write(f"📝 **You:** {chat['content']}")
    else:
        st.write(f"🤖 **Tutor:** {chat['content']}")

# --- Input box ---
user_input = st.text_area(
    "Ask your tutor anything:",
    value=st.session_state["my_input_box"],
    key="my_input_box"
)

# --- Submit button ---
if st.button("Submit"):
    if user_input.strip():
        with st.spinner("Thinking..."):
            # Build context from prior history
            messages = [{"role": "system", "content": "You are an English tutor. Answer clearly and helpfully."}]
            for past in st.session_state["chat_history"]:
                messages.append({"role": past["role"], "content": past["content"]})
            messages.append({"role": "user", "content": user_input})

            # Make the OpenAI call
            response = client.chat.completions.create(
                model="gpt-4.1-nano",
                messages=messages
            )
            answer = response.choices[0].message.content

            # Update chat history
            st.session_state["chat_history"].append({"role": "user", "content": user_input})
            st.session_state["chat_history"].append({"role": "assistant", "content": answer})

            # Update tokens (simple count)
            tokens_used = len(user_input.split()) // 2 + len(answer.split()) // 2
            st.session_state["tokens_remaining"] -= tokens_used

            # Clear input & force re-run to show response immediately
            st.session_state["my_input_box"] = ""
            st.experimental_rerun()
    else:
        st.warning("Please enter a question.")
