import streamlit as st
import sys
import os
import requests
import json
from datetime import datetime, date, timedelta

# Add parent directory to path so we can import backend modules directly
sys.path.append(os.path.abspath('..'))

st.set_page_config(page_title="AI Networking Assistant", layout="wide")

# --- Custom Styling (Injected CSS & Animations) ---
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
        position: relative;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif;
        color: #ffffff !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
    }

    /* Background Blur Glowing Circles */
    .glow-circle-1 {
        position: absolute;
        top: -10%;
        left: 20%;
        width: 300px;
        height: 300px;
        background: rgba(99, 102, 241, 0.12);
        filter: blur(100px);
        border-radius: 50%;
        pointer-events: none;
        z-index: -1;
    }
    .glow-circle-2 {
        position: absolute;
        top: 40%;
        right: 10%;
        width: 400px;
        height: 400px;
        background: rgba(139, 92, 246, 0.1);
        filter: blur(120px);
        border-radius: 50%;
        pointer-events: none;
        z-index: -1;
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #07060f !important;
        border-right: 1px solid rgba(129, 140, 248, 0.1) !important;
    }
    section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
        padding-bottom: 80px !important; /* Elegant scroll margin at the bottom */
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
    
    /* Favorite state card */
    .favorite-card {
        border-color: rgba(245, 158, 11, 0.25) !important;
        background: rgba(35, 26, 15, 0.45) !important;
        box-shadow: 0 8px 32px 0 rgba(245, 158, 11, 0.05) !important;
    }
    .favorite-card:hover {
        border-color: rgba(245, 158, 11, 0.6) !important;
        box-shadow: 0 15px 40px 0 rgba(245, 158, 11, 0.15) !important;
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

    /* Chip Badges for Themes */
    .badge-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-top: 0.5rem;
        margin-bottom: 1.25rem;
    }
    .badge {
        background: rgba(99, 102, 241, 0.08) !important;
        border: 1px solid rgba(99, 102, 241, 0.2) !important;
        color: #a5b4fc !important;
        padding: 0.35rem 0.85rem !important;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
        transition: all 0.2s ease;
        letter-spacing: 0.02em;
    }
    .badge:hover {
        border-color: #818cf8;
        color: #ffffff;
        box-shadow: 0 0 12px rgba(99, 102, 241, 0.3);
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

    /* Action buttons in columns layout */
    div[data-testid="column"] .stButton>button {
        padding: 0.4rem 0.5rem !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        width: 100% !important;
        background: rgba(255, 255, 255, 0.03) !important;
        box-shadow: none !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        color: #94a3b8 !important;
        transition: all 0.2s ease !important;
        text-align: center !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }
    div[data-testid="column"] .stButton>button:hover {
        background: rgba(129, 140, 248, 0.15) !important;
        border-color: rgba(129, 140, 248, 0.4) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 15px rgba(129, 140, 248, 0.2) !important;
        transform: translateY(-1px) !important;
    }

    /* Filter Chips overrides */
    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 9999px !important;
        padding: 0.35rem 1.2rem !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.25) !important;
    }
    .stButton>button[kind="secondary"] {
        background: rgba(255, 255, 255, 0.02) !important;
        color: #94a3b8 !important;
        border: 1px solid rgba(129, 140, 248, 0.1) !important;
        border-radius: 9999px !important;
        padding: 0.35rem 1.2rem !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }
    .stButton>button[kind="secondary"]:hover {
        background: rgba(129, 140, 248, 0.15) !important;
        border-color: rgba(129, 140, 248, 0.4) !important;
        color: #ffffff !important;
        transform: translateY(-1px) !important;
    }

    /* Tab Layout navigation */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px !important;
        background-color: rgba(10, 9, 21, 0.6) !important;
        padding: 8px !important;
        border-radius: 16px !important;
        border: 1px solid rgba(129, 140, 248, 0.1) !important;
        margin-bottom: 2rem !important;
    }
    .stTabs [data-baseweb="tab"] {
        height: 48px !important;
        background-color: transparent !important;
        border-radius: 12px !important;
        color: #64748b !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        border: none !important;
        transition: all 0.2s ease !important;
        padding: 0 24px !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #f1f5f9 !important;
        background-color: rgba(255, 255, 255, 0.03) !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(79, 70, 229, 0.15) !important;
        color: #c7d2fe !important;
        border: 1px solid rgba(99, 102, 241, 0.3) !important;
    }

    /* Responsive full width configuration with compact top padding */
    .block-container {
        padding-top: 1.5rem !important;
        padding-left: 3rem !important;
        padding-right: 3rem !important;
    }

    /* Horizontal Rules (Dividers) */
    hr {
        border: 0 !important;
        height: 1px !important;
        background: linear-gradient(to right, rgba(129, 140, 248, 0), rgba(129, 140, 248, 0.2), rgba(129, 140, 248, 0)) !important;
        margin: 2.5rem 0 !important;
    }

    /* Fade-in Animations */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .fade-in-element {
        animation: fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    /* Responsive adjustments for mobile devices */
    @media (max-width: 768px) {
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        h1 {
            font-size: 2rem !important;
        }
        h2 {
            font-size: 1.5rem !important;
        }
        h3 {
            font-size: 1.25rem !important;
        }
        .custom-card {
            padding: 1.25rem !important;
        }
        /* Make column inputs stack neatly without margins */
        [data-testid="column"] {
            margin-bottom: 0.5rem !important;
        }
        /* Buttons should take full width on mobile for easy tap targets */
        .stButton>button {
            padding: 0.6rem 1rem !important;
            font-size: 0.85rem !important;
        }
        div[data-testid="column"] .stButton>button {
            width: 100% !important;
            padding: 0.5rem 1rem !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Render Background Blur Circles
st.markdown('<div class="glow-circle-1"></div><div class="glow-circle-2"></div>', unsafe_allow_html=True)

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

# Sub-caches for advanced UI logs logic
if "expanded_cards" not in st.session_state:
    st.session_state.expanded_cards = set()
if "favorite_cards" not in st.session_state:
    st.session_state.favorite_cards = set()
if "deleted_cards" not in st.session_state:
    st.session_state.deleted_cards = set()

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
        
    st.markdown("---")
    st.markdown('<p style="font-size:0.8rem; font-weight: 700; color: #4b5563; text-transform: uppercase; margin-bottom: 0.5rem; letter-spacing: 0.05em;">Pro Tips</p>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="custom-card" style="padding: 0.85rem !important; border-left: 3px solid #818cf8; margin-bottom: 0.5rem;">
            <div style="font-weight: 600; font-size: 0.78rem; color: #a5b4fc; display: flex; align-items: center; gap: 6px;">
                Pro Tip
            </div>
            <div style="font-size: 0.72rem; color: #94a3b8; margin-top: 0.2rem; line-height: 1.4;">
                Add specific interests to generate highly personalized conversation starters.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown('<div style="margin-top: 2rem; font-size: 0.8rem; color: #4b5563;">NetAssist v1.4.0</div>', unsafe_allow_html=True)

# --- Top Navigation Bar ---
col_nav, _ = st.columns([1, 2])
with col_nav:
    pages = ["Assistant", "History"]
    active_index = pages.index(st.session_state.active_page) if st.session_state.active_page in pages else 0
    current_page = st.radio("Navigation", pages, index=active_index, horizontal=True, label_visibility="collapsed")
    st.session_state.active_page = current_page

# --- Main App Content ---
if current_page == "Assistant":
    # Hero Landing Experience
    st.markdown(
        """
        <div class="fade-in-element" style="background: rgba(30, 41, 59, 0.2); border: 1px solid rgba(129, 140, 248, 0.1); border-radius: 20px; padding: 2.5rem; margin-bottom: 2rem; backdrop-filter: blur(8px);">
            <h1 style="margin: 0; font-size: 2.4rem; font-family: 'Outfit', sans-serif;">Personalized Networking Assistant</h1>
            <p style="color: #94a3b8; font-size: 1.15rem; margin-top: 0.5rem; margin-bottom: 1.5rem; max-width: 800px; line-height: 1.6;">
                Prepare smarter for conferences, meetups, hackathons, and networking events with AI-generated conversation starters, personalized insights, and real-time fact checking.
            </p>
            <div style="display: flex; gap: 0.75rem; flex-wrap: wrap;">
                <span class="badge" style="background: rgba(79, 70, 229, 0.15); border-color: rgba(79, 70, 229, 0.3); color: #c7d2fe; padding: 0.4rem 1rem;">AI Powered</span>
                <span class="badge" style="background: rgba(16, 185, 129, 0.15); border-color: rgba(16, 185, 129, 0.3); color: #a7f3d0; padding: 0.4rem 1rem;">Instant Responses</span>
                <span class="badge" style="background: rgba(245, 158, 11, 0.15); border-color: rgba(245, 158, 11, 0.3); color: #fde68a; padding: 0.4rem 1rem;">Conversation Planning</span>
                <span class="badge" style="background: rgba(236, 72, 153, 0.15); border-color: rgba(236, 72, 153, 0.3); color: #fbcfe8; padding: 0.4rem 1rem;">Networking Events</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Segmented Tabs Control
    tab1, tab2 = st.tabs(["Conversation Starters", "Quick Fact Check"])
    
    # --- TAB 1: CONVERSATION STARTERS ---
    with tab1:
        st.markdown('<h3 style="margin-top: 0.5rem;">Plan Your Conversations</h3>', unsafe_allow_html=True)
        
        # Friendly AI Welcome Experience & Feature Cards (shown only if no suggestions generated yet)
        if not st.session_state.suggestions:
            st.markdown(
                """
                <div class="custom-card fade-in-element" style="border-left: 4px solid #818cf8; padding: 1.5rem; margin-bottom: 2rem;">
                    <h4 style="margin: 0 0 0.5rem 0; color: #ffffff;">Welcome to NetAssist</h4>
                    <p style="color: #cbd5e1; margin: 0; font-size: 0.95rem; line-height: 1.5;">
                        Prepare for your next networking event in seconds. Enter the details of the event you are attending, add your target interests, and generate tailored starter questions to break the ice instantly.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Feature Cards Row
            st.markdown('<h5 style="color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; font-size: 0.78rem; margin-bottom: 0.75rem;">Explore Features</h5>', unsafe_allow_html=True)
            col_feat1, col_feat2, col_feat3 = st.columns(3)
            with col_feat1:
                st.markdown(
                    """
                    <div class="custom-card" style="padding: 1.25rem !important; height: 100%;">
                        <h5 style="margin: 0 0 0.35rem 0; color: #ffffff;">Conversation Starters</h5>
                        <p style="color: #94a3b8; font-size: 0.82rem; line-height: 1.4; margin: 0;">Generate personalized icebreakers based on your interests and event format.</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with col_feat2:
                st.markdown(
                    """
                    <div class="custom-card" style="padding: 1.25rem !important; height: 100%;">
                        <h5 style="margin: 0 0 0.35rem 0; color: #ffffff;">Quick Fact Check</h5>
                        <p style="color: #94a3b8; font-size: 0.82rem; line-height: 1.4; margin: 0;">Verify tech concepts, companies, or trending topics on Wikipedia before speaking.</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with col_feat3:
                st.markdown(
                    """
                    <div class="custom-card" style="padding: 1.25rem !important; height: 100%;">
                        <h5 style="margin: 0 0 0.35rem 0; color: #ffffff;">Networking Strategy</h5>
                        <p style="color: #94a3b8; font-size: 0.82rem; line-height: 1.4; margin: 0;">Access dynamic stats and logs of past searches to build your event memory.</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            st.markdown('<div style="margin-top: 1.5rem;"></div>', unsafe_allow_html=True)
            
        # Balanced stacked inputs
        event_desc = st.text_area(
            "Describe the event you are attending", 
            placeholder="Describe the event you're attending... (e.g. A tech conference about Generative AI, a startup meetup in Mumbai, etc.)", 
            value=st.session_state.event_desc,
            height=120
        )
        
        user_interests = st.text_input(
            "Your interests (separated by commas)", 
            placeholder="e.g. AI, Startups, Cloud, Marketing"
        )
        
        st.markdown('<div style="margin-top: 0.75rem;"></div>', unsafe_allow_html=True)
        
        # Generate button in a limited columns layout to keep button width proportional
        col_btn, _ = st.columns([1, 2])
        with col_btn:
            generate_clicked = st.button("Get Conversation Starters")

        if generate_clicked:
            if not event_desc or not user_interests:
                st.warning("Please describe both the event and your interests.")
            else:
                interests_list = [i.strip() for i in user_interests.split(',')]
                payload = {
                    "description": event_desc,
                    "interests": interests_list
                }
                
                with st.spinner("Generating AI conversation starters..."):
                    try:
                        headers = {"access_token": st.session_state.access_token}
                        response = requests.post(f"{st.session_state.base_url}/generate-conversation", json=payload, headers=headers)
                        
                        if response.status_code == 200:
                            data = response.json()
                            st.session_state.themes = data.get("topics", [])
                            st.session_state.suggestions = data.get("suggestions", [])
                            st.session_state.event_desc = event_desc
                            st.toast("Conversation starters are ready!")
                        else:
                            st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
                    except Exception as e:
                        st.error(f"Failed to connect to server: {e}")

        # Display Results
        if st.session_state.themes:
            st.markdown("---")
            st.markdown('<h4 style="margin-bottom: 0.5rem;">Key Event Topics</h4>', unsafe_allow_html=True)
            
            badge_html = '<div class="badge-container">'
            for theme in st.session_state.themes:
                badge_html += f'<span class="badge">{theme}</span>'
            badge_html += '</div>'
            st.markdown(badge_html, unsafe_allow_html=True)
            
        if st.session_state.suggestions:
            st.markdown('<h4 style="margin-bottom: 1rem;">Suggested Conversation Starters</h4>', unsafe_allow_html=True)
            
            for i, suggestion in enumerate(st.session_state.suggestions):
                # Dynamic premium AI badges
                category = st.session_state.themes[i % len(st.session_state.themes)] if st.session_state.themes else "General"
                difficulty = ["Easy", "Medium", "Intermediate"][i % 3]
                duration = ["2 min", "3 min", "5 min"][i % 3] + " conversation"
                
                # Render suggestion in a card
                st.markdown(
                    f"""
                    <div class="custom-card fade-in-element">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                            <div class="custom-card-header">Conversation Starter #{i+1}</div>
                            <div style="display: flex; gap: 0.4rem;">
                                <span class="badge" style="font-size: 0.68rem; padding: 0.2rem 0.5rem; background: rgba(79, 70, 229, 0.1); color: #c7d2fe; border: 1px solid rgba(79, 70, 229, 0.2);">{category}</span>
                                <span class="badge" style="font-size: 0.68rem; padding: 0.2rem 0.5rem; background: rgba(16, 185, 129, 0.1); color: #a7f3d0; border: 1px solid rgba(16, 185, 129, 0.2);">{difficulty}</span>
                                <span class="badge" style="font-size: 0.68rem; padding: 0.2rem 0.5rem; background: rgba(245, 158, 11, 0.1); color: #fde68a; border: 1px solid rgba(245, 158, 11, 0.2);">{duration}</span>
                            </div>
                        </div>
                        <div style="font-size: 1.1rem; line-height: 1.6; color: #f1f5f9; font-weight: 500; font-style: italic; margin-bottom: 0.5rem;">
                            "{suggestion}"
                        </div>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                
                # Interactive columns for feedback
                col1, col2, col3 = st.columns([1.5, 1.5, 5])
                with col1:
                    if st.button("Helpful", key=f'like_{i}'):
                        headers = {"access_token": st.session_state.access_token}
                        try:
                            resp = requests.post(f"{st.session_state.base_url}/submit-feedback", json={"user_id": "anonymous", "rating": "like", "comments": suggestion}, headers=headers)
                            if resp.status_code == 200:
                                st.toast("Saved as helpful!")
                            else:
                                st.error("Server error saving feedback.")
                        except Exception as e:
                            st.error(f"Failed to submit feedback: {e}")
                with col2:
                    if st.button("Not Helpful", key=f'dislike_{i}'):
                        headers = {"access_token": st.session_state.access_token}
                        try:
                            resp = requests.post(f"{st.session_state.base_url}/submit-feedback", json={"user_id": "anonymous", "rating": "dislike", "comments": suggestion}, headers=headers)
                            if resp.status_code == 200:
                                st.toast("Saved as not helpful.")
                            else:
                                st.error("Server error saving feedback.")
                        except Exception as e:
                            st.error(f"Failed to submit feedback: {e}")
                st.markdown('<div style="margin-bottom: 1.5rem;"></div>', unsafe_allow_html=True)

    # --- TAB 2: QUICK FACT CHECK ---
    with tab2:
        st.markdown('<h3 style="margin-top: 0.5rem;">Quick Fact Checker</h3>', unsafe_allow_html=True)
        st.write("Type in a topic or technology to verify facts on Wikipedia before speaking about it.")
        
        fact_query = st.text_input("Topic to verify", placeholder="e.g. LLMs, Kubernetes, React, Python")
        
        st.markdown('<div style="margin-top: 0.75rem;"></div>', unsafe_allow_html=True)
        
        col_check_btn, _ = st.columns([1, 2])
        with col_check_btn:
            search_clicked = st.button("Look Up on Wikipedia")

        if search_clicked:
            if fact_query:
                with st.spinner("Checking Wikipedia summaries..."):
                    try:
                        headers = {"access_token": st.session_state.access_token}
                        response = requests.post(f"{st.session_state.base_url}/fact-check", json={"query": fact_query}, headers=headers)
                        if response.status_code == 200:
                            data = response.json()
                            summary = data.get("summary", "No summary found.")
                            
                            st.markdown(
                                f"""
                                <div class="custom-card fade-in-element" style="border-left: 4px solid #10b981; margin-top: 1.5rem;">
                                    <div class="custom-card-header" style="color: #10b981;">Wikipedia Summary for "{fact_query}"</div>
                                    <div style="font-size: 1rem; line-height: 1.6; color: #f1f5f9; margin-top: 0.5rem;">
                                        {summary}
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                        else:
                            st.error("Could not find facts. Make sure the topic is spelled correctly.")
                    except Exception as e:
                        st.error(f"Server connection error: {e}")
            else:
                st.warning("Please enter a topic.")

elif current_page == "History":
    # Hero Section
    st.markdown(
        """
        <div style="background: rgba(30, 41, 59, 0.2); border: 1px solid rgba(129, 140, 248, 0.1); border-radius: 16px; padding: 2rem; margin-bottom: 2rem; backdrop-filter: blur(8px);">
            <h1 style="margin: 0; display: flex; align-items: center; gap: 14px;">Conversation History</h1>
            <p style="color: #94a3b8; font-size: 1.1rem; margin-top: 0.4rem; margin-bottom: 0;">Revisit and continue your previous event conversations.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Load History from backend
    history_entries = []
    try:
        headers = {"access_token": st.session_state.access_token}
        response = requests.get(f"{st.session_state.base_url}/history", headers=headers)
        if response.status_code == 200:
            history_entries = response.json()
    except Exception as e:
        st.error(f"Could not load history from backend: {e}")
        
    # Exclude locally deleted cards
    history_entries = [e for e in history_entries if e.get('timestamp') not in st.session_state.deleted_cards]
    
    if not history_entries:
        # Empty State
        st.markdown(
            """
            <div style="text-align: center; padding: 4rem 2rem; background: rgba(30, 41, 59, 0.15); border-radius: 20px; border: 1px dashed rgba(129, 140, 248, 0.2); margin-top: 2rem;">
                <h3 style="margin-top: 0; color: #ffffff; font-size: 1.5rem;">No conversations yet</h3>
                <p style="color: #94a3b8; font-size: 1rem; max-width: 420px; margin: 0 auto 2rem auto;">Start exploring events to build your AI memory.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        col_empty1, col_empty_btn, col_empty2 = st.columns([1.5, 1, 1.5])
        with col_empty_btn:
            if st.button("Explore Events", key="empty_explore"):
                st.session_state.active_page = "Assistant"
                st.rerun()
                
    else:
        # Dynamic Statistics calculation
        total_convs = len(history_entries)
        ai_events = 0
        startup_events = 0
        cities = set()
        
        known_cities = ["Bangalore", "Mumbai", "Delhi", "Pune", "Hyderabad", "Chennai", "Kolkata", "San Francisco", "New York", "London", "Tokyo", "Berlin", "Paris"]
        
        for entry in history_entries:
            data_dict = entry.get('data', {})
            desc = data_dict.get('event_description', '').lower()
            interests = [i.lower() for i in data_dict.get('user_interests', [])]
            themes = [t.lower() for t in data_dict.get('extracted_themes', [])]
            
            if any(x in desc or any(x in i for i in interests) or any(x in t for t in themes) for x in ["ai", "artificial intelligence", "machine learning", "deep learning", "llm"]):
                ai_events += 1
            if any(x in desc or any(x in i for i in interests) or any(x in t for t in themes) for x in ["startup", "entrepreneur", "founder", "venture capital", "fundraising"]):
                startup_events += 1
            for city in known_cities:
                if city.lower() in desc:
                    cities.add(city)
                    
        cities_count = len(cities) if cities else 1
        
        # Statistics Layout
        col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
        with col_stat1:
            st.markdown(
                f"""
                <div class="custom-card" style="padding: 1rem !important; text-align: center;">
                    <div style="font-size: 0.72rem; color: #818cf8; text-transform: uppercase; font-weight: 600; letter-spacing: 0.05em;">Total Memory</div>
                    <div style="font-size: 1.8rem; font-weight: 700; color: #ffffff; margin-top: 0.25rem;">{total_convs}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col_stat2:
            st.markdown(
                f"""
                <div class="custom-card" style="padding: 1rem !important; text-align: center;">
                    <div style="font-size: 0.72rem; color: #10b981; text-transform: uppercase; font-weight: 600; letter-spacing: 0.05em;">AI Events</div>
                    <div style="font-size: 1.8rem; font-weight: 700; color: #ffffff; margin-top: 0.25rem;">{ai_events}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col_stat3:
            st.markdown(
                f"""
                <div class="custom-card" style="padding: 1rem !important; text-align: center;">
                    <div style="font-size: 0.72rem; color: #f59e0b; text-transform: uppercase; font-weight: 600; letter-spacing: 0.05em;">Startup Events</div>
                    <div style="font-size: 1.8rem; font-weight: 700; color: #ffffff; margin-top: 0.25rem;">{startup_events}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col_stat4:
            st.markdown(
                f"""
                <div class="custom-card" style="padding: 1rem !important; text-align: center;">
                    <div style="font-size: 0.72rem; color: #ec4899; text-transform: uppercase; font-weight: 600; letter-spacing: 0.05em;">Cities Explored</div>
                    <div style="font-size: 1.8rem; font-weight: 700; color: #ffffff; margin-top: 0.25rem;">{cities_count}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        st.markdown('<div style="margin-top: 1.5rem;"></div>', unsafe_allow_html=True)
        
        # Timeline grouping logic
        def get_timeline_group(timestamp_str):
            try:
                dt = datetime.strptime(timestamp_str.split('.')[0], "%Y-%m-%d %H:%M:%S")
                today = date.today()
                entry_date = dt.date()
                
                if entry_date == today:
                    return "Today"
                elif entry_date == today - timedelta(days=1):
                    return "Yesterday"
                elif today - timedelta(days=7) <= entry_date < today - timedelta(days=1):
                    return "Last 7 Days"
                elif today - timedelta(days=30) <= entry_date < today - timedelta(days=7):
                    return "Last Month"
                else:
                    return "Older"
            except:
                return "Older"
                
        timeline_order = ["Today", "Yesterday", "Last 7 Days", "Last Month", "Older"]
        grouped_history = {group: [] for group in timeline_order}
        
        for entry in history_entries:
            group = get_timeline_group(entry.get('timestamp', ''))
            grouped_history[group].append(entry)
            
        # Render Grouped Cards
        for group in timeline_order:
            entries_in_group = grouped_history[group]
            if not entries_in_group:
                continue
                
            # Timeline Group Header
            st.markdown(
                f"""
                <div style="display: flex; gap: 1rem; align-items: center; margin-top: 2rem; margin-bottom: 1rem;">
                    <div style="width: 8px; height: 8px; border-radius: 50%; background-color: #818cf8; box-shadow: 0 0 10px #818cf8;"></div>
                    <h4 style="margin: 0; font-family: 'Outfit', sans-serif; text-transform: uppercase; font-size: 0.8rem; letter-spacing: 0.1em; color: #818cf8;">{group}</h4>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Render Cards inside this Group
            for entry in entries_in_group:
                timestamp = entry.get('timestamp', '')
                data_dict = entry.get('data', {})
                desc = data_dict.get('event_description', '')
                
                # Generate dynamic event details
                # Format title
                title_fmt = "Networking Event"
                desc_lower = desc.lower()
                topics_list = data_dict.get('extracted_themes', [])
                topic = topics_list[0] if topics_list else (data_dict.get('user_interests', [])[0] if data_dict.get('user_interests', []) else "Networking")
                
                if "workshop" in desc_lower:
                    title_fmt = f"{topic} Workshop"
                elif "meetup" in desc_lower:
                    title_fmt = f"{topic} Meetup"
                elif "conference" in desc_lower:
                    title_fmt = f"{topic} Conference"
                elif "panel" in desc_lower:
                    title_fmt = f"{topic} Panel Discussion"
                else:
                    title_fmt = f"{topic} Gathering"
                    
                # Time formatting
                try:
                    dt = datetime.strptime(timestamp.split('.')[0], "%Y-%m-%d %H:%M:%S")
                    date_str = dt.strftime("%B %d, %Y")
                    time_str = dt.strftime("%I:%M %p")
                except:
                    date_str, time_str = "Recent Date", "Recent Time"
                    
                # Location
                location = "Virtual / TBD"
                for city in known_cities:
                    if city.lower() in desc_lower:
                        location = city
                        break
                        
                # Toggle details expand
                is_expanded = timestamp in st.session_state.expanded_cards
                is_favorite = timestamp in st.session_state.favorite_cards
                
                # Summary truncation
                summary_text = desc
                if not is_expanded and len(desc) > 160:
                    summary_text = desc[:157] + "..."
                    
                # Tag badges
                interests_badges = ""
                for i in data_dict.get('user_interests', []):
                    interests_badges += f'<span class="badge" style="background: rgba(129, 140, 248, 0.08); border-color: rgba(129, 140, 248, 0.2); color: #a5b4fc;">{i}</span>'
                for t in data_dict.get('extracted_themes', []):
                    interests_badges += f'<span class="badge" style="background: rgba(16, 185, 129, 0.08); border-color: rgba(16, 185, 129, 0.2); color: #a7f3d0;">{t}</span>'
                    
                # Render card HTML
                fav_class = " favorite-card" if is_favorite else ""
                st.markdown(
                    f"""
                    <div class="custom-card{fav_class}">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 0.75rem;">
                            <div style="display: flex; align-items: center; gap: 10px;">
                                <h4 style="margin: 0; font-size: 1.1rem; color: #ffffff;">{title_fmt}</h4>
                            </div>
                            <div style="font-size: 0.8rem; color: #64748b; font-weight: 500;">
                                <span>Date: {date_str}</span> &nbsp;&bull;&nbsp; <span>Time: {time_str}</span> &nbsp;&bull;&nbsp; <span>Location: {location}</span>
                            </div>
                        </div>
                        <div style="font-size: 0.95rem; line-height: 1.6; color: #cbd5e1; margin-bottom: 1rem;">
                            {summary_text}
                        </div>
                        <div class="badge-container">
                            {interests_badges}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                # Footer actions: 4 columns
                col_act1, col_act2, col_act3, col_act4 = st.columns(4)
                
                with col_act1:
                    if st.button("Continue", key=f"continue_{timestamp}"):
                        st.session_state.event_desc = desc
                        st.session_state.suggestions = data_dict.get('generated_suggestions', [])
                        st.session_state.themes = data_dict.get('extracted_themes', [])
                        st.session_state.active_page = "Assistant"
                        st.rerun()
                with col_act2:
                    details_label = "Hide Details" if is_expanded else "View Details"
                    if st.button(details_label, key=f"details_{timestamp}"):
                        if is_expanded:
                            st.session_state.expanded_cards.remove(timestamp)
                        else:
                            st.session_state.expanded_cards.add(timestamp)
                        st.rerun()
                with col_act3:
                    fav_label = "Unfavorite" if is_favorite else "Favorite"
                    if st.button(fav_label, key=f"fav_{timestamp}"):
                        if is_favorite:
                            st.session_state.favorite_cards.remove(timestamp)
                        else:
                            st.session_state.favorite_cards.add(timestamp)
                        st.rerun()
                with col_act4:
                    if st.button("Delete", key=f"del_{timestamp}"):
                        st.session_state.deleted_cards.add(timestamp)
                        st.toast("Conversation removed from memory.")
                        st.rerun()
                        
                st.markdown('<div style="margin-bottom: 1.5rem;"></div>', unsafe_allow_html=True)
