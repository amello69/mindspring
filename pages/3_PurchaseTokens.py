import streamlit as st

if "logged_in_user" not in st.session_state:
    st.warning("Please log in from the main page.")
    st.stop()

st.title("💳 Purchase More Tokens")
st.write("Select a package to top up your tokens.")

option = st.selectbox(
    "Token packages",
    ["100 tokens - $5", "500 tokens - $20", "1000 tokens - $35"]
)

if st.button("Purchase"):
    if "100" in option:
        st.session_state["tokens_remaining"] += 100
    elif "500" in option:
        st.session_state["tokens_remaining"] += 500
    elif "1000" in option:
        st.session_state["tokens_remaining"] += 1000
    st.success(f"Purchase successful! Your new balance is {st.session_state['tokens_remaining']} tokens.")
    st.balloons()
