import streamlit as st

if "logged_in_user" not in st.session_state:
    st.warning("Please log in from the main page.")
    st.stop()

st.title("👤 Your Profile")

username = st.session_state.get("logged_in_user", "")
name = st.session_state.get("logged_in_name", "")
tokens_remaining = st.session_state.get("tokens_remaining", 0)
monthly_tokens = st.session_state.get("monthly_tokens", 1000)

st.write(f"Welcome, **{name}** (username: `{username}`)!")
st.write(f"**Monthly tokens assigned:** {monthly_tokens}")
st.write(f"**Tokens remaining this month:** {tokens_remaining}")

if tokens_remaining <= 0:
    st.error("You have exhausted your monthly tokens. Please purchase more.")

if st.button("Purchase more tokens"):
    st.switch_page("pages/3_PurchaseTokens.py")
