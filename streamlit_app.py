import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

# --- AUTHENTICATION ---
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
if not status:
    st.stop()  # stays on login page if not authenticated

# Only after login does navigation load
from pages import profile, tutor

pages = [
    st.Page(profile.run, title="Profile", icon="👤", default=True),
    st.Page(tutor.run, title="Tutor", icon="🗣️"),
]

page = st.navigation(pages, position="sidebar")
page.run()
