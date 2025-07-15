import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI"]["API_KEY"])

# --- Auth check ---
if "logged_in_user" not in st.session_state:
    st.warning("Please log in from the main page.")
    st.stop()

# --- Init state ---
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "input_key_counter" not in st.session_state:
    st.session_state["input_key_counter"] = 0

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

# --- Display chat history ---
for chat in st.session_state["chat_history"]:
    if chat["role"] == "user":
        st.write(f"📝 **You:** {chat['content']}")
    else:
        st.write(f"🤖 **Tutor:** {chat['content']}")

# --- Use key increment trick ---
input_key = f"input_box_{st.session_state['input_key_counter']}"
user_input = st.text_area("Ask your tutor anything:", key=input_key)

if st.button("Submit"):
    if user_input.strip():
        with st.spinner("Thinking..."):
            # Build full message list
            messages = [{"role": "system", "content": "You are an English tutor."}]
            for past in st.session_state["chat_history"]:
                messages.append({"role": past["role"], "content": past["content"]})
            messages.append({"role": "user", "content": user_input})

            # Call OpenAI
            response = client.chat.completions.create(
                model="gpt-4.1-nano",
                messages=messages
            )
            answer = response.choices[0].message.content

            # Update chat & tokens
            st.session_state["chat_history"].append({"role": "user", "content": user_input})
            st.session_state["chat_history"].append({"role": "assistant", "content": answer})
            tokens_used = len(user_input.split()) // 2 + len(answer.split()) // 2
            st.session_state["tokens_remaining"] -= tokens_used
            st.success(f"Tokens used: {tokens_used}. Remaining: {st.session_state['tokens_remaining']}")

            # ✅ Force new input box by bumping key
            st.session_state["input_key_counter"] += 1
            st.experimental_rerun()
    else:
        st.warning("Please enter a question.")
