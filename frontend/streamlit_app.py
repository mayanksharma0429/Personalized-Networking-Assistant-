import streamlit as st
import sys
import os
import requests
import json

# Add parent directory to path so we can import backend modules directly
sys.path.append(os.path.abspath('..'))

st.set_page_config(page_title="AI Networking Assistant", layout="wide")

# --- Custom Styling (Injected CSS) ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

    html, body, [data-testid="stAppViewContainer"], .main {
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #f8fafc;
    }

    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at 50% 0%, #17153b 0%, #0a0915 75%) !important;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif;
        color: #ffffff !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
    }

    /* Card Layouts (Glassmorphic) */
    .custom-card {
        background: rgba(22, 21, 44, 0.6) !important;
        border: 1px solid rgba(129, 140, 248, 0.1) !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        margin-bottom: 0.75rem !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37) !important;
        backdrop-filter: blur(8px) !important;
        -webkit-backdrop-filter: blur(8px) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    .custom-card:hover {
        transform: translateY(-2px) !important;
        border-color: rgba(129, 140, 248, 0.3) !important;
        box-shadow: 0 12px 40px 0 rgba(99, 102, 241, 0.15) !important;
    }

    .custom-card-header {
        font-weight: 600;
        color: #818cf8;
        margin-bottom: 0.5rem;
        font-family: 'Outfit', sans-serif;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    /* Custom form elements styling override */
    .stTextArea textarea, .stTextInput input {
        background-color: rgba(10, 9, 21, 0.8) !important;
        color: #f8fafc !important;
        border: 1px solid rgba(129, 140, 248, 0.15) !important;
        border-radius: 12px !important;
        padding: 0.75rem 1rem !important;
        transition: all 0.3s ease !important;
        font-size: 0.95rem !important;
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #818cf8 !important;
        box-shadow: 0 0 15px rgba(129, 140, 248, 0.2) !important;
        background-color: rgba(10, 9, 21, 0.95) !important;
    }

    /* Primary actions buttons */
    .stButton>button {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.75rem !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        letter-spacing: 0.03em !important;
        box-shadow: 0 4px 20px rgba(79, 70, 229, 0.3) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px rgba(79, 70, 229, 0.5) !important;
        border-color: rgba(255, 255, 255, 0.25) !important;
    }
    .stButton>button:active {
        transform: translateY(1px) !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Configuration
BASE_URL = "http://127.0.0.1:8000"

st.title("Personalized Networking Assistant")
st.write("Generate conversation starters and fact-check topics for your next event!")

# --- Session State Initialization ---
if "suggestions" not in st.session_state:
    st.session_state.suggestions = []
if "event_desc" not in st.session_state:
    st.session_state.event_desc = ""
if "themes" not in st.session_state:
    st.session_state.themes = []

# --- Generation Section ---
st.header("Plan Your Conversations")

event_desc = st.text_area("Event Description", placeholder="e.g., A tech meetup in Bangalore for AI developers.")
user_interests = st.text_input("Your Interests", placeholder="e.g., AI, marketing, startups (comma separated)")

if st.button("Generate Ideas"):
    if not event_desc or not user_interests:
        st.warning("Please provide both event description and your interests.")
    else:
        # Process interests: compact but important piece of data cleaning
        interests_list = [i.strip() for i in user_interests.split(',')]
        
        # We still use the API for generation, since backend runs the heavy AI models
        payload = {
            "description": event_desc,
            "interests": interests_list
        }
        
        with st.spinner("Analyzing event & generating topics..."):
            try:
                # The API needs the access token
                headers = {"access_token": "my_super_secret_api_key_123"}
                response = requests.post(f"{BASE_URL}/generate-conversation", json=payload, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    st.session_state.themes = data.get("topics", [])
                    st.session_state.suggestions = data.get("suggestions", [])
                    st.session_state.event_desc = event_desc
                else:
                    st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"Failed to connect to backend: {e}")

# Display results dynamically if suggestions exist in session state
if "suggestions" in st.session_state and st.session_state.suggestions:
    st.subheader("Extracted Themes")
    for theme in st.session_state.themes:
        st.markdown(f"- {theme}")
        
    st.subheader("Conversation Starters & Feedback")
    
    # Loop through suggestions and render them with thumbs up/down
    for i, suggestion in enumerate(st.session_state.suggestions):
        st.markdown(f"**{i+1}.** {suggestion}")
        
        # Dynamic responsive layout using st.columns
        col1, col2, _ = st.columns([1.5, 1.5, 10])
        
        with col1:
            if st.button("Helpful", key=f'like_{i}'):
                headers = {"access_token": "my_super_secret_api_key_123"}
                requests.post(f"{BASE_URL}/submit-feedback", json={"user_id": "anonymous", "rating": "like", "comments": suggestion}, headers=headers)
                st.toast("Feedback saved!")
        with col2:
            if st.button("Not Helpful", key=f'dislike_{i}'):
                headers = {"access_token": "my_super_secret_api_key_123"}
                requests.post(f"{BASE_URL}/submit-feedback", json={"user_id": "anonymous", "rating": "dislike", "comments": suggestion}, headers=headers)
                st.toast("Feedback saved!")

st.markdown('---')

# --- Fact Checking Section ---
st.header("Quick Fact Check")
fact_query = st.text_input("Enter a topic to quickly verify before you speak about it:")

if st.button("Search Wikipedia"):
    if fact_query:
        with st.spinner("Checking facts..."):
            try:
                headers = {"access_token": "my_super_secret_api_key_123"}
                response = requests.post(f"{BASE_URL}/fact-check", json={"query": fact_query}, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    # Render the fact-check result in a green highlighted box
                    st.success(data.get("summary", "No summary found."))
                else:
                    st.error("Could not retrieve facts.")
            except Exception as e:
                st.error("Backend error.")
    else:
        st.warning("Please enter a topic.")

st.markdown('---')

# --- History Section ---
st.header("Conversation History")
try:
    headers = {"access_token": "my_super_secret_api_key_123"}
    response = requests.get(f"{BASE_URL}/history", headers=headers)
    if response.status_code == 200:
        recent_history = response.json()
        if recent_history:
            for entry in recent_history:
                data_dict = entry.get('data', {})
                st.markdown(f"**Event:** {data_dict.get('event_description', 'N/A')}")
                
                # Clean up the interests list display
                interests = data_dict.get('user_interests', 'N/A')
                interests_str = ", ".join(interests) if isinstance(interests, list) else str(interests)
                st.markdown(f"**Interests:** {interests_str}")
                
                st.markdown(f"*Themes:* {', '.join(data_dict.get('extracted_themes', []))}")
                st.markdown("---")
        else:
            st.info("No history found.")
    else:
        st.info("No history found.")
except Exception as e:
    st.error("Could not load history.")

st.markdown('---')

# --- Feedback History Section ---
st.header("Feedback History")
try:
    headers = {"access_token": "my_super_secret_api_key_123"}
    response = requests.get(f"{BASE_URL}/feedback", headers=headers)
    if response.status_code == 200:
        recent_feedbacks = response.json()
        if recent_feedbacks:
            for entry in recent_feedbacks:
                data = entry.get('feedback', {})
                timestamp = entry.get('timestamp', '')
                
                # Ternary expression for visual indicator
                rating = data.get('rating', '')
                icon = "Helpful:" if rating == 'like' else "Not Helpful:" if rating == 'dislike' else rating
                
                st.markdown(f"{icon} {data.get('comments', 'N/A')}")
                # Render metadata in a subdued font
                st.caption(f"Time: {timestamp}")
        else:
            st.info("No feedback found.")
    else:
        st.info("No feedback found.")
except Exception as e:
    st.error("Could not load feedback history.")
