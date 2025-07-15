import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI"]["API_KEY"])

def write_history_to_file(history, filename="chat_history.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for chat in history:
            role = "You" if chat["role"] == "user" else "Tutor"
            f.write(f"{role}: {chat['content']}\n")

def read_history_from_file(filename="chat_history.txt"):
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
if "pending_user_input" not in st.session_state:
    st.session_state["pending_user_input"] = None

st.title("🗣️ AI English Tutor")

tokens_remaining = st.session_state.get("tokens_remaining", 0)
st.sidebar.markdown(f"**Tokens remaining:** {tokens_remaining}")

if st.button("🗑️ Clear Chat"):
    st.session_state["chat_history"] = []
    write_history_to_file(st.session_state["chat_history"])  # clear file too
    st.success("Chat history cleared!")

# --- Always write history to file and display it above the form
write_history_to_file(st.session_state["chat_history"])
history_text = read_history_from_file()
st.subheader("Chat Transcript")
st.text(history_text)

disable_input = tokens_remaining <= 0
if disable_input:
    st.error("You have exhausted your monthly tokens. Please purchase more to continue.")

# --- Input form ---
with st.form(key="input_form", clear_on_submit=True):
    user_input = st.text_area(
        "Ask your tutor anything:",
        key="input_text",
        disabled=disable_input
    )
    submitted = st.form_submit_button("Submit", disabled=disable_input)
    if submitted and user_input.strip():
        st.session_state["pending_user_input"] = user_input

# --- Process after form submission ---
if st.session_state.get("pending_user_input"):
    user_input = st.session_state["pending_user_input"]
    with st.spinner("Thinking..."):
        messages = [{"role": "system", "content": "You are an English tutor. Answer clearly and helpfully."}]
        for past in st.session_state["chat_history"]:
            messages.append({"role": past["role"], "content": past["content"]})
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

        # Write updated history after each response
        write_history_to_file(st.session_state["chat_history"])

    st.session_state["pending_user_input"] = None
