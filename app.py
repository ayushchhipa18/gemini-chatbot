import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import uuid

# Load API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel("models/gemini-1.5-flash")

st.set_page_config(page_title="Chatur Bot", layout="centered")
st.markdown("<h1 style='text-align: center;'>👾 Chatur Bot 👾</h1>", unsafe_allow_html=True)

# --- Login Logic ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.session_state.input_key = str(uuid.uuid4())  # Set unique key for input box
            st.rerun()
        else:
            st.error("Invalid credentials")
    st.stop()

# --- Chat history ---
if "history" not in st.session_state:
    st.session_state.history = []

if "input_key" not in st.session_state:
    st.session_state.input_key = str(uuid.uuid4())


# --- Message handler ---
def handle_message(user_input):
    user_input = user_input.strip()
    if user_input:
        st.session_state.history.append(("You", user_input))
        try:
            response = model.generate_content(user_input)
            st.session_state.history.append(("Gemini", response.text))
        except Exception as e:
            st.session_state.history.append(("Gemini", f"❌ Error: {e}"))
        st.session_state.input_key = str(uuid.uuid4())  # Change key to clear input


# --- Show chat ---
for speaker, msg in st.session_state.history:
    st.markdown(f"**{speaker}:** {msg}")

st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)

# --- Input box + Send button ---
col1, col2 = st.columns([5, 1])
with col1:
    user_input = st.text_input(
        "You:",
        key=st.session_state.input_key,  # dynamic key
        placeholder="Ask anything...",
        label_visibility="collapsed",
    )
with col2:
    if st.button("Send"):
        handle_message(user_input)
