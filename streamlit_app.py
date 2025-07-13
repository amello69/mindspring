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

if not st.session_state.get("authentication_status"):
    st.stop()

# Streamlit's st.navigation actually expects st.Page objects that are either:
#   - functions (like page_profile) with unique signatures
#   - or file paths with Python scripts containing `if __name__ == "__page__":` blocks

# Safer fallback using string file paths:
pages = [
    "pages/profile.py",
    "pages/tutor.py"
]

current_page = st.navigation(pages, position="sidebar")
current_page.run()
