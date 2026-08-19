import streamlit as st
from sqlalchemy.orm import Session
from database.models import User
from utils.constants import STATES_LIST, OCCUPATIONS, EDUCATION_LEVELS, UI_TEXT

def render_profile_page(db: Session, current_user_profile: dict, language: str = "English"):
    txt = UI_TEXT.get(language, UI_TEXT["English"])

    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%); padding: 25px; border-radius: 16px; color: white; margin-bottom: 25px; border: 1px solid #3a506b; box-shadow: 0 10px 25px rgba(37,99,235,0.2);">
            <h2 style="margin: 0; font-weight: 800; color: #ffffff;">👤 {txt.get('profile_title')}</h2>
            <p style="font-size: 1rem; color: #e2e8f0; margin-top: 5px;">{txt.get('profile_desc')}</p>
        </div>
    """, unsafe_allow_html=True)

    # 1-Click Demo Preset Loader
    col_hdr1, col_hdr2 = st.columns([3, 1])
    with col_hdr2:
        if st.button(f"🔄 {txt.get('reset_demo')}", use_container_width=True):
            user = db.query(User).filter_by(is_demo=True).first()
            if user:
                user.name = "Demo Student"
                user.age = 19
                user.gender = "General"
                user.state = "Uttar Pradesh"
                user.district = "Lucknow"
                user.occupation = "Student"
                user.is_student = True
                user.education_level = "B.Tech"
                user.annual_family_income = 250000.0
                user.area_type = "Urban"
                user.category_type = "General"
                db.commit()
                st.success("Loaded Demo Student profile (Age: 19, UP, B.Tech, Income: ₹2,50,000)!")
                st.rerun()

    with st.form("citizen_profile_form"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input(txt.get("full_name"), value=current_user_profile.get("name", "Demo Student"))
            age = st.number_input(txt.get("age"), min_value=1, max_value=100, value=int(current_user_profile.get("age", 19)))
            gender = st.selectbox(
                txt.get("gender"), 
                ["General", "Female", "Male", "Other"],
                index=0
            )
            state_idx = STATES_LIST.index(current_user_profile.get("state", "Uttar Pradesh")) if current_user_profile.get("state") in STATES_LIST else 0
            state = st.selectbox(txt.get("state"), STATES_LIST, index=state_idx)
            district = st.text_input(txt.get("district"), value=current_user_profile.get("district", "Lucknow"))
            category_type = st.selectbox(
                txt.get("category"),
                ["General", "OBC", "SC", "ST", "EWS"],
                index=0
            )

        with col2:
            occ_idx = OCCUPATIONS.index(current_user_profile.get("occupation", "Student")) if current_user_profile.get("occupation") in OCCUPATIONS else 0
            occupation = st.selectbox(txt.get("occupation"), OCCUPATIONS, index=occ_idx)
            is_student = st.checkbox(txt.get("is_student"), value=bool(current_user_profile.get("is_student", True)))
            edu_idx = EDUCATION_LEVELS.index(current_user_profile.get("education_level", "Undergraduate (B.Tech / B.Sc / B.A / B.Com)")) if current_user_profile.get("education_level") in EDUCATION_LEVELS else 3
            education_level = st.selectbox(txt.get("education"), EDUCATION_LEVELS, index=edu_idx)
            income = st.number_input(
                txt.get("income"), 
                min_value=0.0, 
                max_value=10000000.0, 
                value=float(current_user_profile.get("annual_family_income", 250000.0)),
                step=10000.0
            )
            area_type = st.radio(txt.get("area"), ["Urban", "Rural"], index=0 if current_user_profile.get("area_type") == "Urban" else 1, horizontal=True)

        submitted = st.form_submit_button(txt.get("save_profile"), type="primary", use_container_width=True)

        if submitted:
            user = db.query(User).filter_by(id=current_user_profile.get("id", 1)).first()
            if not user:
                user = User(is_demo=True)
                db.add(user)
            
            user.name = name
            user.age = age
            user.gender = gender
            user.state = state
            user.district = district
            user.occupation = occupation
            user.is_student = is_student
            user.education_level = education_level
            user.annual_family_income = income
            user.area_type = area_type
            user.category_type = category_type

            db.commit()
            st.success("Citizen Profile successfully updated in SQLite database!")
            st.rerun()
