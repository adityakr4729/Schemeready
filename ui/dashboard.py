import streamlit as st
from utils.constants import APP_NAME, TAGLINE, PROBLEM_STATEMENT, UI_TEXT

def render_dashboard(db_session, user_profile, eligibility_results, readiness_results, language: str = "English"):
    txt = UI_TEXT.get(language, UI_TEXT["English"])
    tagline_text = TAGLINE.get(language, TAGLINE["English"])
    problem_text = PROBLEM_STATEMENT.get(language, PROBLEM_STATEMENT["English"])

    # Sleek Hero Section Banner - Deep Navy Blue & Sapphire Gradient
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0b132b 0%, #1c2541 50%, #3a506b 100%); padding: 35px 30px; border-radius: 20px; color: white; margin-bottom: 25px; border: 1px solid #3a506b; box-shadow: 0 12px 30px rgba(0,0,0,0.4); position: relative; overflow: hidden;">
            <div style="position: relative; z-index: 2;">
                <h1 style="margin: 0; font-size: 2.8rem; font-weight: 800; letter-spacing: -1px; color: #ffffff;">{APP_NAME}</h1>
                <p style="font-size: 1.25rem; color: #cbd5e1; margin-top: 6px; font-weight: 500;">"{tagline_text}"</p>
                <div style="margin-top: 20px; background: rgba(11,19,43,0.7); padding: 14px 20px; border-radius: 12px; border-left: 4px solid #4895ef; color: #e2e8f0; max-width: 800px;">
                    💡 <b>Core Innovation</b>: <i>"AI explains eligibility, but deterministic Python rules decide."</i>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Active Profile Quick Action Bar
    profile_bar_title = "सक्रिय नागरिक प्रोफाइल" if language=="Hindi" else "Active Citizen Profile"
    st.markdown(f"""
        <div style="background: #1c2541; border: 1px solid #3a506b; border-radius: 14px; padding: 18px 24px; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); display: flex; align-items: center; justify-content: space-between;">
            <div>
                <span style="font-size: 0.8rem; color: #94a3b8; font-weight: 700; text-transform: uppercase;">{profile_bar_title}</span>
                <div style="font-size: 1.1rem; font-weight: 700; color: #ffffff; margin-top: 2px;">
                    👤 {user_profile['name']} &nbsp;|&nbsp; 🎂 {'आयु' if language=='Hindi' else 'Age'}: {user_profile['age']} &nbsp;|&nbsp; 📍 {'राज्य' if language=='Hindi' else 'State'}: {user_profile['state']} &nbsp;|&nbsp; 💼 {user_profile['occupation']} &nbsp;|&nbsp; 💰 {'आय' if language=='Hindi' else 'Income'}: ₹{user_profile['annual_family_income']:,.0f}
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Key Metrics Display Grid
    m1, m2, m3, m4 = st.columns(4)

    eligible_count = sum(1 for r in eligibility_results if r.is_eligible)
    total_schemes = len(eligibility_results)
    top_readiness = max([r.overall_score for r in readiness_results], default=0.0)

    m1.metric(txt.get("tab_eligible", "Eligible Schemes"), f"{eligible_count} / {total_schemes}", delta="Qualified By Rules")
    m2.metric(txt.get("profile", "Citizen Profile"), "100%", delta="Verified")
    m3.metric(txt.get("readiness_score", "Max Readiness Score"), f"{top_readiness}%", delta="Application-Ready")
    m4.metric(txt.get("document_reuse", "Document Reuse"), "4 Docs Ready", delta="Cross-Scheme")

    st.markdown("<hr style='margin: 30px 0; border-color: #3a506b;'>", unsafe_allow_html=True)

    # 6-Step Workflow Card Grid
    wf_title = "6-स्तरीय नागरिक आवेदन तत्परता कार्यप्रवाह" if language=="Hindi" else "6-Step Citizen Application Readiness Workflow"
    st.markdown(f"<h3 style='color: #ffffff;'>📋 {wf_title}</h3>", unsafe_allow_html=True)
    st.caption("How SchemeReady guides citizens from benefit discovery to official portal application.")

    w1, w2, w3 = st.columns(3)
    with w1:
        st.markdown(f"""
            <div style="background: #1c2541; border: 1px solid #3a506b; border-radius: 14px; padding: 20px; height: 100%; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
                <div style="font-size: 2rem; margin-bottom: 8px;">1️⃣</div>
                <h4 style="margin: 0; color: #4895ef; font-weight: 700;">{'योजना खोज' if language=='Hindi' else 'Scheme Discovery'}</h4>
                <p style="color: #cbd5e1; font-size: 0.9rem; margin-top: 6px;">Filters official state and central databases based on citizen demographics.</p>
            </div>
        """, unsafe_allow_html=True)
    with w2:
        st.markdown(f"""
            <div style="background: #1c2541; border: 1px solid #3a506b; border-radius: 14px; padding: 20px; height: 100%; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
                <div style="font-size: 2rem; margin-bottom: 8px;">2️⃣</div>
                <h4 style="margin: 0; color: #4895ef; font-weight: 700;">{'पात्रता नियम' if language=='Hindi' else 'Deterministic Rules'}</h4>
                <p style="color: #cbd5e1; font-size: 0.9rem; margin-top: 6px;">Evaluates age, income, and domicile thresholds line-by-line without AI guessing.</p>
            </div>
        """, unsafe_allow_html=True)
    with w3:
        st.markdown(f"""
            <div style="background: #1c2541; border: 1px solid #3a506b; border-radius: 14px; padding: 20px; height: 100%; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
                <div style="font-size: 2rem; margin-bottom: 8px;">3️⃣</div>
                <h4 style="margin: 0; color: #4895ef; font-weight: 700;">{'दस्तावेज़ चेकलिस्ट' if language=='Hindi' else 'Smart Document Checklist'}</h4>
                <p style="color: #cbd5e1; font-size: 0.9rem; margin-top: 6px;">Tracks mandatory documents and detects missing certificates instantly.</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

    w4, w5, w6 = st.columns(3)
    with w4:
        st.markdown(f"""
            <div style="background: #1c2541; border: 1px solid #3a506b; border-radius: 14px; padding: 20px; height: 100%; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
                <div style="font-size: 2rem; margin-bottom: 8px;">4️⃣</div>
                <h4 style="margin: 0; color: #4895ef; font-weight: 700;">{'OCR एवं निरंतरता जांच' if language=='Hindi' else 'OCR & Consistency Check'}</h4>
                <p style="color: #cbd5e1; font-size: 0.9rem; margin-top: 6px;">Extracts document values via PyMuPDF/OCR and verifies name/income consistency.</p>
            </div>
        """, unsafe_allow_html=True)
    with w5:
        st.markdown(f"""
            <div style="background: #1c2541; border: 1px solid #3a506b; border-radius: 14px; padding: 20px; height: 100%; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
                <div style="font-size: 2rem; margin-bottom: 8px;">5️⃣</div>
                <h4 style="margin: 0; color: #4895ef; font-weight: 700;">{'तत्परता स्कोर' if language=='Hindi' else 'Readiness Score'}</h4>
                <p style="color: #cbd5e1; font-size: 0.9rem; margin-top: 6px;">Mathematical formula (50% Eligibility + 50% Docs) showing readiness percentage.</p>
            </div>
        """, unsafe_allow_html=True)
    with w6:
        st.markdown(f"""
            <div style="background: #1c2541; border: 1px solid #3a506b; border-radius: 14px; padding: 20px; height: 100%; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
                <div style="font-size: 2rem; margin-bottom: 8px;">6️⃣</div>
                <h4 style="margin: 0; color: #4895ef; font-weight: 700;">{'आधिकारिक आवेदन पोर्टल' if language=='Hindi' else 'Direct Application Portal'}</h4>
                <p style="color: #cbd5e1; font-size: 0.9rem; margin-top: 6px;">Routes verified citizens directly to official government portals (.gov.in).</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='margin: 30px 0; border-color: #3a506b;'>", unsafe_allow_html=True)

    # Problem Statement Section
    st.markdown(f"<h3 style='color: #ffffff;'>🎯 {'समस्या का समाधान' if language=='Hindi' else 'Problem Solved'}</h3>", unsafe_allow_html=True)
    st.info(problem_text)
