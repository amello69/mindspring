import sys
import os
import streamlit as st

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
