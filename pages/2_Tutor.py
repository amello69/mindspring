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

# --- Always allow clearing chat ---
if st.button("🗑️ Clear Chat"):
    st.session_state["chat_history"] = []
    st.success("Chat history cleared!")

# --- Display chat history first ---
for chat in st.session_state["chat_history"]:
    if chat["role"] == "user":
        st.write(f"📝 **You:** {chat['content']}")
    else:
        st.write(f"🤖 **Tutor:** {chat['content']}")

# --- Only disable input if out of tokens ---
disable_input = tokens_remaining <= 0
if disable_input:
    st.error("You have exhausted your monthly tokens. Please purchase more to continue.")

# --- Input & submit always appear after history ---
with st.container():
    input_key = f"my_input_box_{st.session_state['input_key_counter']}"
    user_input = st.text_area("Ask your tutor anything:", key=input_key, disabled=disable_input)

    if st.button("Submit", disabled=disable_input):
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

                # ✅ Increment key immediately to shift input below on this run
                st.session_state["input_key_counter"] += 1

                st.write(f"🤖 **Tutor:** {answer}")

                tokens_used = len(user_input.split()) // 2 + len(answer.split()) // 2
                st.session_state["tokens_remaining"] -= tokens_used
                st.success(f"Tokens used: {tokens_used}. Remaining: {st.session_state['tokens_remaining']}")
                st.session_state["input_key_counter"] += 1
                st.experimental_rerun()
        else:
            st.warning("Please enter a question.")
