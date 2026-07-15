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

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #07060f !important;
        border-right: 1px solid rgba(129, 140, 248, 0.1) !important;
    }
    
    section[data-testid="stSidebar"] p {
        color: #94a3b8;
    }

    /* Horizontal Navigation Bar styling at the top of the page */
    .stRadio > div[role="radiogroup"] {
        flex-direction: row !important;
        background-color: rgba(22, 21, 44, 0.6) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(129, 140, 248, 0.1) !important;
        padding: 4px !important;
        gap: 8px !important;
        display: inline-flex !important;
        margin-bottom: 2rem !important;
    }
    .stRadio label {
        padding: 6px 16px !important;
        border-radius: 8px !important;
        color: #94a3b8 !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
        border: none !important;
    }
    .stRadio label:hover {
        background-color: rgba(255, 255, 255, 0.03) !important;
        color: #ffffff !important;
    }
    /* Active state for horizontal navigation */
    .stRadio div[role="radiogroup"] > label[data-checked="true"] {
        background-color: rgba(79, 70, 229, 0.15) !important;
        color: #c7d2fe !important;
        border: 1px solid rgba(99, 102, 241, 0.3) !important;
    }
    /* Hide default radio marker circle globally (multiple selectors for version safety) */
    .stRadio label div[data-testid="stMarker"],
    .stRadio label > div:first-child,
    .stRadio div[role="radiogroup"] label > div:first-child,
    .stRadio label span[class*="stMarker"] {
        display: none !important;
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

    /* Page container top padding spacing fix */
    .block-container {
        padding-top: 1.5rem !important;
        padding-left: 3rem !important;
        padding-right: 3rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Session State Initialization ---
if "suggestions" not in st.session_state:
    st.session_state.suggestions = []
if "event_desc" not in st.session_state:
    st.session_state.event_desc = ""
if "themes" not in st.session_state:
    st.session_state.themes = []
if "base_url" not in st.session_state:
    st.session_state.base_url = "http://127.0.0.1:8000"
if "access_token" not in st.session_state:
    st.session_state.access_token = "my_super_secret_api_key_123"
if "active_page" not in st.session_state:
    st.session_state.active_page = "Assistant"

# --- Sidebar Configuration ---
with st.sidebar:
    st.markdown('<h2 style="font-family:\'Outfit\', sans-serif; display: flex; align-items: center; gap: 10px;">NetAssist</h2>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:0.9rem; margin-bottom: 1.5rem;">Your personalized AI-powered networking assistant to guide you through meetups and conferences.</p>', unsafe_allow_html=True)
    
    # Redesigned settings card
    st.markdown(
        """
        <div class="custom-card" style="padding: 1rem !important; border: 1px solid rgba(129, 140, 248, 0.15); margin-bottom: 0.5rem;">
            <div style="font-weight: 600; font-size: 0.85rem; color: #ffffff; display: flex; align-items: center; gap: 8px;">
                Settings
            </div>
            <div style="font-size: 0.72rem; color: #94a3b8; margin-top: 0.2rem;">
                Configure connection settings for the local server.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    api_url = st.text_input("Server Address", value=st.session_state.base_url)
    token = st.text_input("Security Key", value=st.session_state.access_token, type="password")
    
    st.session_state.base_url = api_url.strip()
    st.session_state.access_token = token.strip()

# --- Top Navigation Bar ---
col_nav, _ = st.columns([1, 2])
with col_nav:
    pages = ["Assistant", "History"]
    active_index = pages.index(st.session_state.active_page) if st.session_state.active_page in pages else 0
    current_page = st.radio("Navigation", pages, index=active_index, horizontal=True, label_visibility="collapsed")
    st.session_state.active_page = current_page

# --- Main App Content ---
if current_page == "Assistant":
    st.title("Personalized Networking Assistant")
    st.write("Generate conversation starters and fact-check topics for your next event!")
    
    # --- Generation Section ---
    st.header("Plan Your Conversations")
    
    event_desc = st.text_area("Event Description", placeholder="e.g., A tech meetup in Bangalore for AI developers.")
    user_interests = st.text_input("Your Interests", placeholder="e.g., AI, marketing, startups (comma separated)")
    
    if st.button("Generate Ideas"):
        if not event_desc or not user_interests:
            st.warning("Please provide both event description and your interests.")
        else:
            interests_list = [i.strip() for i in user_interests.split(',')]
            payload = {
                "description": event_desc,
                "interests": interests_list
            }
            
            with st.spinner("Analyzing event & generating topics..."):
                try:
                    headers = {"access_token": st.session_state.access_token}
                    response = requests.post(f"{st.session_state.base_url}/generate-conversation", json=payload, headers=headers)
                    
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
                    headers = {"access_token": st.session_state.access_token}
                    requests.post(f"{BASE_URL}/submit-feedback", json={"user_id": "anonymous", "rating": "like", "comments": suggestion}, headers=headers)
                    st.toast("Feedback saved!")
            with col2:
                if st.button("Not Helpful", key=f'dislike_{i}'):
                    headers = {"access_token": st.session_state.access_token}
                    requests.post(f"{BASE_URL}/submit-feedback", json={"user_id": "anonymous", "rating": "dislike", "comments": suggestion}, headers=headers)
                    st.toast("Feedback saved!")

elif current_page == "History":
    st.title("Conversation History")
    st.write("Revisit and continue your previous event conversations.")
    st.markdown("---")
    
    try:
        headers = {"access_token": st.session_state.access_token}
        response = requests.get(f"{st.session_state.base_url}/history", headers=headers)
        if response.status_code == 200:
            recent_history = response.json()
            if recent_history:
                for entry in recent_history:
                    data_dict = entry.get('data', {})
                    st.markdown(f"**Event:** {data_dict.get('event_description', 'N/A')}")
                    
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
