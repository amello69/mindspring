import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

# Load credentials
with open("credentials.yaml") as f:
    config = yaml.load(f, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
    auto_hash=False,
)

authenticator.login(location="main")

status = st.session_state.get("authentication_status")

if status is True:
    # ✅ Save stable session values you control
    if "logged_in_user" not in st.session_state:
        st.session_state["logged_in_user"] = st.session_state.get("username", "")
        st.session_state["logged_in_name"] = st.session_state.get("name", "")
elif status is False:
    st.error("Incorrect username/password")
    st.stop()
else:
    st.warning("Please log in to continue")
    st.stop()

# --- Navigation after login ---
pages = [
    "pages/profile.py",
    "pages/tutor.py"
]

current_page = st.navigation(pages, position="sidebar")
current_page.run()
