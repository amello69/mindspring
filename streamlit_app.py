# streamlit_app.py
import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

# Load credentials and create authenticator
with open("credentials.yaml") as f:
    config = yaml.load(f, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
    config.get("preauthorized"),
    auto_hash=False  # Set according to your use of hashed passwords
)

# Show login in the main area
authenticator.login(location="main")

# Check login status in session_state
status = st.session_state.get("authentication_status")
name = st.session_state.get("name", "")

if not status:
    # Not authenticated—you'll remain on login page
    st.stop()

# ✅ User is authenticated — proceed to multipage navigation
from pages import profile, tutor

pages = [
    st.Page(profile.run, title="Profile", icon="👤", default=True),
    st.Page(tutor.run, title="Tutor", icon="🗣️")
]

page = st.navigation(pages, position="sidebar")
page.run()
