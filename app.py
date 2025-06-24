import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Load Gemini model
model = genai.GenerativeModel("models/gemini-1.5-flash")

# Page title
st.set_page_config(page_title="Chatur Bot", layout="centered")
st.markdown("<h1 style='text-align: center;'>👾Chatur Bot 👾</h1>", unsafe_allow_html=True)

# --- Session States ---
if "history" not in st.session_state:
    st.session_state.history = []
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# --- Login UI ---
if not st.session_state.logged_in:
    with st.form("login_form"):
        st.subheader("🔐 Please Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Login")

        if login_button:
            if username == "admin" and password == "1234":
                st.session_state.logged_in = True
                st.success("✅ Login successful! Now you can chat.")
                st.rerun()

            else:
                st.error("❌ Invalid credentials. Try again.")

# --- Chatbot UI (Only after login) ---
if st.session_state.logged_in:
    # --- Function to handle submission ---
    def handle_submit():
        user_input = st.session_state.input_text.strip()
        if user_input:
            st.session_state.history.append(("You", user_input))
            try:
                response = model.generate_content(user_input)
                st.session_state.history.append(("Gemini", response.text))
            except Exception as e:
                st.session_state.history.append(("Gemini", f"❌ Error: {e}"))
        st.session_state.input_text = ""

    # Show chat history
    for speaker, msg in st.session_state.history:
        st.markdown(f"**{speaker}:** {msg}")

    # Add spacer to push input to bottom
    st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)

    # Input section at bottom
    col1, col2 = st.columns([5, 1])
    with col1:
        st.text_input(
            label="You:",
            key="input_text",
            placeholder="Ask anything...",
            on_change=handle_submit,
            label_visibility="collapsed",
        )
    with col2:
        if st.button("Send"):
            handle_submit()
