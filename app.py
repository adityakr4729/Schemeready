import os
import sys

# Ensure local lib folder is on python path
LIB_DIR = os.path.join(os.path.dirname(__file__), "lib")
if LIB_DIR not in sys.path:
    sys.path.insert(0, LIB_DIR)

import json
import streamlit as st

# Configure page with custom favicon & layout
st.set_page_config(
    page_title="SchemeReady — Citizen Benefit Readiness Platform",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Navy Blue Deep Dark Theme for SIH Grand Finale
st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">

    <style>
    /* Main Background & Text Color - Deep Navy Blue */
    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background-color: #0b132b !important;
        color: #f8fafc !important;
    }

    /* Top Tricolor Brand Line */
    .stAppViewContainer::before {
        content: "";
        display: block;
        height: 5px;
        width: 100%;
        background: linear-gradient(90deg, #FF9933 0%, #FFFFFF 50%, #128807 100%);
        position: fixed;
        top: 0;
        left: 0;
        z-index: 9999;
    }

    /* Sidebar Dark Navy Styling */
    [data-testid="stSidebar"] {
        background-color: #1c2541 !important;
        border-right: 1px solid #3a506b !important;
    }
    
    /* Ensure ALL text in Sidebar is crisp white and fully visible */
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
        color: #f8fafc !important;
    }

    /* Sidebar Radio Button Styling */
    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        background-color: #0b132b !important;
        border: 1px solid #3a506b !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        margin-bottom: 6px !important;
        transition: all 0.2s ease !important;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
        border-color: #4895ef !important;
        background-color: #162040 !important;
    }

    /* Buttons Styling */
    .stButton>button {
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        padding: 10px 20px !important;
        transition: all 0.2s ease-in-out !important;
    }
    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #4895ef 0%, #3f37c9 100%) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(72, 149, 239, 0.4) !important;
    }
    .stButton>button[kind="secondary"] {
        background: #1c2541 !important;
        color: #f8fafc !important;
        border: 1px solid #3a506b !important;
    }

    /* Form Input Controls - Dark Navy inputs */
    div[data-baseweb="select"] > div, 
    .stTextInput input, 
    .stNumberInput input,
    .stTextArea textarea {
        background-color: #1c2541 !important;
        color: #ffffff !important;
        border: 1px solid #3a506b !important;
        border-radius: 8px !important;
    }

    /* Metric Cards Styling */
    [data-testid="stMetric"] {
        background: #1c2541 !important;
        border: 1px solid #3a506b !important;
        border-radius: 14px !important;
        padding: 18px 20px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25) !important;
        border-top: 4px solid #4895ef !important;
    }
    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-size: 0.85rem !important;
        font-weight: 700 !important;
        text-transform: uppercase;
    }
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 1.8rem !important;
        font-weight: 800 !important;
    }

    /* Expanders & Tabs in Dark Theme */
    .stExpander {
        background-color: #1c2541 !important;
        border: 1px solid #3a506b !important;
        border-radius: 10px !important;
    }
    button[data-baseweb="tab"] {
        color: #cbd5e1 !important;
        font-weight: 600 !important;
    }
    button[aria-selected="true"] {
        color: #4895ef !important;
        border-bottom-color: #4895ef !important;
    }

    /* Hide Default Header/Footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

from database.database import SessionLocal, init_db
from database.seed_data import seed_database
from database.models import Scheme, User
from utils.helpers import get_current_user_profile, get_user_documents
from utils.constants import APP_NAME, TAGLINE, UI_TEXT
from services.eligibility_engine import RuleEngine
from services.readiness_engine import ReadinessEngine
from services.ai_service import AIService

# UI Renderers
from ui.dashboard import render_dashboard
from ui.profile import render_profile_page
from ui.schemes import render_schemes_page
from ui.documents import render_documents_page
from ui.readiness import render_readiness_page
from ui.deadlines import render_deadlines_and_reuse_page

# Ensure database is initialized & seeded
seed_database(force=False)

def main():
    db = SessionLocal()

    try:
        # Load user profile & documents from DB
        user_profile = get_current_user_profile(db)
        user_docs = get_user_documents(db, user_profile["id"])

        # Load schemes from DB
        schemes_db = db.query(Scheme).all()
        all_schemes = []
        for s in schemes_db:
            rules = [{"field": r.field, "operator": r.operator, "value": r.value, "label": r.label, "failure_reason": r.failure_reason} for r in s.eligibility_rules]
            docs = [{"doc_id": d.doc_id, "name": d.name, "description": d.description, "mandatory": d.mandatory} for d in s.required_documents]
            all_schemes.append({
                "scheme_id": s.scheme_id,
                "scheme_name": s.scheme_name,
                "ministry": s.ministry,
                "department": s.department,
                "state": s.state,
                "category": s.category,
                "description": s.description,
                "benefits": s.benefits,
                "eligibility_rules": rules,
                "required_documents": docs,
                "deadline": s.deadline,
                "renewal_required": s.renewal_required,
                "renewal_information": s.renewal_information,
                "application_url": s.application_url,
                "official_source_url": s.official_source_url,
                "last_updated": s.last_updated
            })

        # Compute Rule Eligibility & Readiness Scores
        eligibility_results = []
        readiness_results = []
        readiness_map = {}

        for s in all_schemes:
            eval_res = RuleEngine.evaluate_scheme(user_profile, s)
            eligibility_results.append(eval_res)

            read_res = ReadinessEngine.calculate_readiness(
                eval_res.is_eligible,
                s.get("required_documents", []),
                user_docs
            )
            read_res.scheme_id = s["scheme_id"]
            read_res.scheme_name = s["scheme_name"]

            readiness_results.append(read_res)
            readiness_map[s["scheme_id"]] = read_res

        # Sidebar Header Branding
        with st.sidebar:
            st.markdown("""
                <div style="text-align: center; padding: 10px 0 15px 0;">
                    <div style="background: linear-gradient(135deg, #4895ef 0%, #3f37c9 100%); width: 60px; height: 60px; border-radius: 16px; margin: 0 auto; display: flex; align-items: center; justify-content: center; box-shadow: 0 8px 16px rgba(72,149,239,0.4);">
                        <span style="font-size: 30px;">🏛️</span>
                    </div>
                    <h2 style="margin: 12px 0 2px 0; color: #ffffff; font-weight: 800;">SchemeReady</h2>
                    <p style="font-size: 0.8rem; color: #94a3b8; font-weight: 600; margin: 0;">SIH Citizen Readiness Engine</p>
                </div>
            """, unsafe_allow_html=True)

            # Language Selection Dropdown
            language = st.selectbox("🌐 Select UI Language", ["English", "Hindi", "Hinglish"], index=0)
            txt = UI_TEXT.get(language, UI_TEXT["English"])

            st.markdown("<hr style='margin: 15px 0; border-color: #3a506b;'>", unsafe_allow_html=True)

            # Standard module mapping for navigation
            nav_mapping = {
                "Home Dashboard": txt.get("home", "Home Dashboard"),
                "Citizen Profile": "Citizen Profile" if language=="English" else "नागरिक प्रोफाइल" if language=="Hindi" else "Citizen Profile",
                "Find Benefits For Me": txt.get("find_benefits", "Find Benefits For Me"),
                "Document Readiness": txt.get("doc_readiness", "Document Readiness"),
                "Application Readiness": txt.get("readiness_score", "Application Readiness"),
                "Deadlines & Renewals": txt.get("deadlines", "Deadlines & Renewals"),
                "AI Scheme Assistant": txt.get("ai_assistant", "AI Scheme Assistant")
            }

            # Reverse map to identify standard internal key
            reverse_nav = {v: k for k, v in nav_mapping.items()}

            if "active_tab" not in st.session_state:
                st.session_state["active_tab"] = "Home Dashboard"

            current_display_label = nav_mapping.get(st.session_state["active_tab"], "Home Dashboard")
            menu_display_list = list(nav_mapping.values())

            selected_display = st.radio(
                "NAVIGATION MODULES" if language=="English" else "नेविगेशन मॉड्यूल्स" if language=="Hindi" else "NAVIGATION MODULES",
                menu_display_list,
                index=menu_display_list.index(current_display_label) if current_display_label in menu_display_list else 0
            )

            st.session_state["active_tab"] = reverse_nav.get(selected_display, "Home Dashboard")

            st.markdown("<hr style='margin: 15px 0; border-color: #3a506b;'>", unsafe_allow_html=True)

            # User Profile Quick Badge in Sidebar
            st.markdown(f"""
                <div style="background: #0b132b; border: 1px solid #3a506b; border-radius: 12px; padding: 14px; margin-bottom: 15px;">
                    <div style="font-size: 0.75rem; color: #94a3b8; font-weight: 700; text-transform: uppercase; margin-bottom: 6px;">
                        {'ACTIVE PROFILE' if language=='English' else 'सक्रिय नागरिक प्रोफाइल' if language=='Hindi' else 'ACTIVE PROFILE'}
                    </div>
                    <div style="font-weight: 700; color: #ffffff; font-size: 0.95rem;">👤 {user_profile['name']} ({user_profile['age']}y)</div>
                    <div style="font-size: 0.82rem; color: #cbd5e1; margin-top: 4px;">📍 {user_profile['state']}</div>
                    <div style="font-size: 0.82rem; color: #cbd5e1;">💼 {user_profile['occupation']} (₹{user_profile['annual_family_income']:,.0f})</div>
                </div>
            """, unsafe_allow_html=True)

            if st.button("🔄 Reset SIH Demo Flow", use_container_width=True):
                seed_database(force=True)
                st.session_state["active_tab"] = "Home Dashboard"
                st.rerun()

            st.markdown("""
                <div style="text-align: center; margin-top: 15px; font-size: 0.75rem; color: #64748b;">
                    🇮🇳 Smart India Hackathon Prototype<br>
                    Verified Government Data Engine
                </div>
            """, unsafe_allow_html=True)

        # Main Page Routing
        active = st.session_state["active_tab"]

        if active == "Home Dashboard":
            render_dashboard(db, user_profile, eligibility_results, readiness_results, language)

        elif active == "Citizen Profile":
            render_profile_page(db, user_profile, language)

        elif active == "Find Benefits For Me":
            render_schemes_page(db, user_profile, all_schemes, readiness_map)

        elif active == "Document Readiness":
            render_documents_page(db, user_profile, user_docs)

        elif active == "Application Readiness":
            render_readiness_page(readiness_results, all_schemes)

        elif active == "Deadlines & Renewals":
            user_avail_doc_ids = [d["doc_id"] for d in user_docs if d["status"] in ["Available", "Verified", "READY", "Ready"]]
            render_deadlines_and_reuse_page(all_schemes, user_avail_doc_ids)

        elif active == "AI Scheme Assistant":
            render_ai_assistant_page(user_profile, all_schemes, language, user_docs)

    finally:
        db.close()

def render_ai_assistant_page(user_profile: dict, all_schemes: list, language: str, user_docs: list):
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1c2541 0%, #0b132b 100%); padding: 25px; border-radius: 16px; color: white; margin-bottom: 25px; border: 1px solid #3a506b;">
            <h2 style="margin: 0; font-weight: 800; color: #4895ef;">🤖 AI Scheme Assistant</h2>
            <p style="font-size: 1rem; color: #cbd5e1; margin-top: 5px;">
                {'Aap sarkari yojanaon, zaroori dastavezon aur last dates ke baare me sawaal pooch sakte hain.' if language in ['Hindi', 'Hinglish'] else 'Ask questions about eligibility conditions, missing documents, or scheme deadlines.'}
            </p>
        </div>
    """, unsafe_allow_html=True)

    ai_active = AIService.is_ai_available()
    if ai_active:
        st.success("🟢 Gemini API Key detected! Powered by Google Gemini AI with local database RAG context.")
    else:
        st.info("ℹ️ Running in **Offline Local RAG Mode** (Deterministic knowledge base). Set `GEMINI_API_KEY` in `.env` to enable Gemini API calls.")

    st.markdown("#### 💡 Quick Prompt Suggestions:")

    if "ai_query" not in st.session_state:
        st.session_state["ai_query"] = "Which schemes suit me?"

    btn1_txt = "Mujhe kaun si yojana milegi?" if language in ["Hindi", "Hinglish"] else "Which schemes suit me?"
    btn2_txt = "Konse documents missing hain?" if language in ["Hindi", "Hinglish"] else "Which documents am I missing?"
    btn3_txt = "Last date kab hai?" if language in ["Hindi", "Hinglish"] else "When are scheme deadlines?"

    c1, c2, c3 = st.columns(3)
    if c1.button(btn1_txt, use_container_width=True):
        st.session_state["ai_query"] = btn1_txt
    if c2.button(btn2_txt, use_container_width=True):
        st.session_state["ai_query"] = btn2_txt
    if c3.button(btn3_txt, use_container_width=True):
        st.session_state["ai_query"] = btn3_txt

    user_query = st.text_input("Type your question:", value=st.session_state["ai_query"])

    if st.button("⚡ Ask Assistant", type="primary", use_container_width=True) or user_query:
        query_to_run = user_query if user_query else st.session_state["ai_query"]
        with st.spinner("Searching scheme knowledge base..."):
            ans_res = AIService.answer_question(query_to_run, user_profile, all_schemes, language, user_docs)
            
            st.markdown(f"""
                <div style="background: #1c2541; border: 1px solid #3a506b; border-radius: 14px; padding: 22px; margin-top: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.3);">
                    <h3 style="color: #4895ef; margin-top: 0;">💬 Answer ({ans_res['mode']})</h3>
                    <div style="font-size: 1.05rem; line-height: 1.6; color: #f8fafc;">{ans_res['answer']}</div>
                    <hr style="margin: 15px 0; border-color: #3a506b;">
                    <span style="font-size: 0.85rem; color: #94a3b8; font-weight: 600;">📌 Source: {ans_res['source']}</span>
                </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
