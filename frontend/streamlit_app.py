import streamlit as st
import sys
import os
import requests
import json

# Add parent directory to path so we can import backend modules directly
sys.path.append(os.path.abspath('..'))
from app.services.feedback_logger import log_feedback

# Configuration
BASE_URL = "http://127.0.0.1:8000"
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
HISTORY_FILE = os.path.join(PROJECT_ROOT, "history.json")
FEEDBACK_FILE = os.path.join(PROJECT_ROOT, "feedback.json")

st.set_page_config(page_title="AI Networking Assistant", page_icon="🤝", layout="wide")

st.title("🤝 Personalized Networking Assistant")
st.write("Generate conversation starters and fact-check topics for your next event!")

# --- Session State Initialization ---
if "suggestions" not in st.session_state:
    st.session_state.suggestions = []
if "event_desc" not in st.session_state:
    st.session_state.event_desc = ""
if "themes" not in st.session_state:
    st.session_state.themes = []

# --- Generation Section ---
st.header("🎯 Plan Your Conversations")

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
        col1, col2, _ = st.columns([1, 1, 10])
        
        with col1:
            if st.button("👍", key=f'like_{i}'):
                # Directly using backend logger instead of API
                log_feedback({"user_id": "anonymous", "rating": "like", "comments": suggestion})
                st.toast("Feedback saved!")
        with col2:
            if st.button("👎", key=f'dislike_{i}'):
                # Directly using backend logger
                log_feedback({"user_id": "anonymous", "rating": "dislike", "comments": suggestion})
                st.toast("Feedback saved!")

st.markdown('---')

# --- Fact Checking Section ---
st.header("🔍 Quick Fact Check")
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
st.header("🕒 Conversation History")
try:
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)
            
        # Slice the five most recent entries and reverse them
        recent_history = list(reversed(history[-5:]))
        
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
st.header("⭐ Feedback History")
try:
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, "r") as f:
            feedbacks = json.load(f)
            
        # Show up to 10 recent feedback entries
        recent_feedbacks = list(reversed(feedbacks[-10:]))
        
        if recent_feedbacks:
            for entry in recent_feedbacks:
                data = entry.get('feedback', {})
                timestamp = entry.get('timestamp', '')
                
                # Ternary expression for visual indicator
                rating = data.get('rating', '')
                icon = "👍" if rating == 'like' else "👎" if rating == 'dislike' else rating
                
                st.markdown(f"{icon} {data.get('comments', 'N/A')}")
                # Render metadata in a subdued font
                st.caption(f"Time: {timestamp}")
        else:
            st.info("No feedback found.")
    else:
        st.info("No feedback found.")
except Exception as e:
    st.error("Could not load feedback history.")
