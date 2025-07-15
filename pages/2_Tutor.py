import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI"]["API_KEY"])

HISTORY_FILENAME = "chat_history.txt"

def write_history_to_file(history, filename=HISTORY_FILENAME):
    with open(filename, "w", encoding="utf-8") as f:
        for chat in history:
            role = "You" if chat["role"] == "user" else "Tutor"
            f.write(f"{role}: {chat['content']}\n")

def read_history_from_file(filename=HISTORY_FILENAME):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""

if "logged_in_user" not in st.session_state:
    st.warning("Please log in from the main page.")
    st.stop()

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""

if "tokens_remaining" not in st.session_state:
    st.session_state["tokens_remaining"] = 1000

st.title("🗣️ AI English Tutor")

tokens_remaining = st.session_state["tokens_remaining"]
st.sidebar.markdown(f"**Tokens remaining:** {tokens_remaining}")

if st.button("🗑️ Clear Chat"):
    st.session_state["chat_history"] = []
    write_history_to_file(st.session_state["chat_history"])
    st.success("Chat history cleared!")

# --- Always write history to file and show above input
write_history_to_file(st.session_state["chat_history"])
history_text = read_history_from_file()
st.subheader("Chat Transcript")
st.text(history_text if history_text else "No conversation yet.")

disable_input = tokens_remaining <= 0
if disable_input:
    st.error("You have exhausted your monthly tokens. Please purchase more to continue.")

user_input = st.text_area(
    "Ask your tutor anything:",
    key="user_input",
    value=st.session_state["user_input"],
    disabled=disable_input,
    height=80,
)

if st.button("Submit", disabled=disable_input):
    if user_input.strip():
        with st.spinner("Thinking..."):
            messages = [{"role": "system", "content": "You are an English tutor. Answer clearly and helpfully."}]
            for chat in st.session_state["chat_history"]:
                messages.append({"role": chat["role"], "content": chat["content"]})
            messages.append({"role": "user", "content": user_input})

            response = client.chat.completions.create(
                model="gpt-4.1-nano",
                messages=messages
            )
            answer = response.choices[0].message.content

            st.session_state["chat_history"].append({"role": "user", "content": user_input})
            st.session_state["chat_history"].append({"role": "assistant", "content": answer})

            tokens_used = len(user_input.split()) // 2 + len(answer.split()) // 2
            st.session_state["tokens_remaining"] -= tokens_used
            st.success(f"Tokens used: {tokens_used}. Remaining: {st.session_state['tokens_remaining']}")

            write_history_to_file(st.session_state["chat_history"])

        # Clear input after submit
        st.session_state["user_input"] = ""
        st.experimental_rerun()  # Rerun to update transcript and clear input
    else:
        st.warning("Please enter a question.")
