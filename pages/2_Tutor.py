import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI"]["API_KEY"])

if "logged_in_user" not in st.session_state:
    st.warning("Please log in from the main page.")
    st.stop()

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if "input_text" not in st.session_state:
    st.session_state["input_text"] = ""

st.title("🗣️ AI English Tutor")

tokens_remaining = st.session_state.get("tokens_remaining", 0)
st.sidebar.markdown(f"**Tokens remaining:** {tokens_remaining}")

if st.button("🗑️ Clear Chat"):
    st.session_state["chat_history"] = []
    st.success("Chat history cleared!")

for chat in st.session_state["chat_history"]:
    if chat["role"] == "user":
        st.write(f"📝 **You:** {chat['content']}")
    else:
        st.write(f"🤖 **Tutor:** {chat['content']}")

disable_input = tokens_remaining <= 0
if disable_input:
    st.error("You have exhausted your monthly tokens. Please purchase more to continue.")

# --- Input box and submit button ---
with st.form(key="input_form", clear_on_submit=True):
    user_input = st.text_area(
        "Ask your tutor anything:",
        key="input_text",
        value=st.session_state["input_text"],
        disabled=disable_input
    )
    submitted = st.form_submit_button("Submit", disabled=disable_input)

    if submitted:
        if user_input.strip():
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
        else:
            st.warning("Please enter a question.")
