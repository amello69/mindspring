import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI"]["API_KEY"])

if "logged_in_user" not in st.session_state:
    st.warning("Please log in from the main page.")
    st.stop()

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

st.title("🗣️ AI English Tutor")
username = st.session_state.get("logged_in_user", "")
name = st.session_state.get("logged_in_name", "")
tokens_remaining = st.session_state.get("tokens_remaining", 0)

st.sidebar.markdown(f"**Tokens remaining:** {tokens_remaining}")

if tokens_remaining <= 0:
    st.error("You have exhausted your monthly tokens. Please purchase more.")
    st.stop()

# ✅ Add a clear chat button
if st.button("🗑️ Clear Chat"):
    st.session_state["chat_history"] = []
    st.success("Chat history cleared!")

# Display the chat history
for chat in st.session_state["chat_history"]:
    if chat["role"] == "user":
        st.write(f"📝 **You:** {chat['content']}")
    else:
        st.write(f"🤖 **Tutor:** {chat['content']}")

# Chat input
user_input = st.text_area("Ask your tutor anything:")

if st.button("Submit"):
    if user_input.strip():
        with st.spinner("Thinking..."):
            # Build complete conversation for context
            messages = [{"role": "system", "content": "You are an English tutor. Answer clearly and helpfully."}]
            for past in st.session_state["chat_history"]:
                messages.append({"role": past["role"], "content": past["content"]})
            messages.append({"role": "user", "content": user_input})
            
            # Call the model
            response = client.chat.completions.create(
                model="gpt-4.1-nano",
                messages=messages
            )
            answer = response.choices[0].message.content
            
            # Update chat history
            st.session_state["chat_history"].append({"role": "user", "content": user_input})
            st.session_state["chat_history"].append({"role": "assistant", "content": answer})
            
            # Update tokens after successful response
            tokens_used = len(user_input.split()) // 2 + len(answer.split()) // 2
            st.session_state["tokens_remaining"] -= tokens_used
            st.info(f"Tokens used: {tokens_used}. Remaining: {st.session_state['tokens_remaining']}")
    else:
        st.warning("Please enter a question.")
