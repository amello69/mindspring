import sys
import os
import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

# Load credentials file
with open("credentials.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
    config.get("preauthorized"),
    auto_hash=False
)

# Render login widget
# name, auth_status, username = authenticator.login("main")
authenticator.login(location="main")
# Then read the status from session_state
status = st.session_state.get("authentication_status")
name = st.session_state.get("name")
username = st.session_state.get("username")

if status:
    st.sidebar.success(f"Welcome {name}")
elif status is False:
    st.sidebar.error("Incorrect username or password")
    st.stop()
else:
    st.sidebar.warning("Please log in to continue")
    st.stop()



if not auth_status:
    st.warning("Please log in.")
    st.stop()

# Make shared modules importable from 'pages/' by adding the project root to sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Now you can safely import auth_utils or other shared modules
from auth_utils import login

# Authentication wrapper
login()

# If not logged in, display welcome screen and stop
if not st.session_state.get("logged_in"):
    st.title("🌱 Welcome to English Tutor")
    st.write("Please log in to continue.")
    st.stop()

# Import pages now that the path is set
import pages.tutor as tutor_page
import pages.profile as profile_page

# Configure navigation
pagelist = [
    st.Page(tutor_page.run, title="Tutor", icon="🗣️", default=True),
    st.Page(profile_page.run, title="Profile", icon="👤")
]
page = st.navigation(pagelist, position="sidebar")
page.run()
