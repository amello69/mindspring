# gen_hashes.py
import streamlit_authenticator as stauth

passwords = ["alice_password", "bob_password"]
hashed = stauth.Hasher(passwords).generate()
print(hashed)
