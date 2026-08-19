import streamlit as st
from services.eligibility_engine import RuleEngine, EligibilityResult
from services.deadline_service import DeadlineService
from utils.helpers import format_currency

def render_schemes_page(db_session, user_profile: dict, all_schemes: list, readiness_map: dict):
    st.markdown("""
        <div style="background: linear-gradient(135deg, #1c2541 0%, #0b132b 100%); padding: 25px; border-radius: 16px; color: white; margin-bottom: 25px; border: 1px solid #3a506b;">
            <h2 style="margin: 0; font-weight: 800; color: #4895ef;">🎯 Find Benefits For Me</h2>
            <p style="font-size: 1rem; color: #cbd5e1; margin-top: 5px;">Rule-based eligibility matching your profile against official government schemes.</p>
        </div>
    """, unsafe_allow_html=True)

    if not all_schemes:
        st.warning("No schemes found in database.")
        return

    # Filter controls
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        category_filter = st.selectbox("Filter by Category", ["All Categories"] + sorted(list(set(s["category"] for s in all_schemes))))
    with col_f2:
        status_filter = st.selectbox("Filter by Eligibility Status", ["All Results", "Eligible Only", "Not Eligible Only"])

    # Evaluate all schemes using Rule Engine
    evaluated_list = []
    for s in all_schemes:
        eval_result = RuleEngine.evaluate_scheme(user_profile, s)
        readiness = readiness_map.get(s["scheme_id"])
        deadline_info = DeadlineService.get_deadline_status(s.get("deadline"))
        
        evaluated_list.append({
            "scheme": s,
            "result": eval_result,
            "readiness": readiness,
            "deadline": deadline_info
        })

    # Filter by user selection
    filtered_list = evaluated_list
    if category_filter != "All Categories":
        filtered_list = [item for item in filtered_list if item["scheme"]["category"] == category_filter]
    if status_filter == "Eligible Only":
        filtered_list = [item for item in filtered_list if item["result"].is_eligible]
    elif status_filter == "Not Eligible Only":
        filtered_list = [item for item in filtered_list if not item["result"].is_eligible]

    # Categorize into Eligible and Not Eligible
    eligible_items = [i for i in filtered_list if i["result"].is_eligible]
    ineligible_items = [i for i in filtered_list if not i["result"].is_eligible]

    # Tabs for Eligible vs Ineligible
    tab1, tab2 = st.tabs([f"✅ Qualified & Eligible ({len(eligible_items)})", f"❌ Not Eligible ({len(ineligible_items)})"])

    with tab1:
        if not eligible_items:
            st.info("No eligible schemes found for current filter settings.")
        else:
            for item in eligible_items:
                _render_scheme_card(item)

    with tab2:
        if not ineligible_items:
            st.info("No ineligible schemes under current filter settings.")
        else:
            for item in ineligible_items:
                _render_scheme_card(item)

def _render_scheme_card(item: dict):
    scheme = item["scheme"]
    res: EligibilityResult = item["result"]
    readiness = item["readiness"]
    dl = item["deadline"]

    status_badge = '<span style="background: #166534; color: #4ade80; padding: 4px 12px; border-radius: 9999px; font-weight: 700; font-size: 0.85rem;">ELIGIBLE ✅</span>' if res.is_eligible else '<span style="background: #991b1b; color: #fca5a5; padding: 4px 12px; border-radius: 9999px; font-weight: 700; font-size: 0.85rem;">NOT ELIGIBLE ❌</span>'

    st.markdown(f"""
        <div style="background: #1c2541; border: 1px solid #3a506b; border-radius: 16px; padding: 24px; margin-bottom: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.3);">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                <div>
                    <span style="background: #1e3a8a; color: #60a5fa; padding: 4px 12px; border-radius: 9999px; font-size: 0.8rem; font-weight: 700;">{scheme['category']}</span>
                    <span style="background: #0f172a; color: #94a3b8; border: 1px solid #3a506b; padding: 4px 12px; border-radius: 9999px; font-size: 0.8rem; font-weight: 700; margin-left: 6px;">{scheme['state']}</span>
                    <h3 style="margin: 10px 0 4px 0; color: #ffffff; font-weight: 800; font-size: 1.35rem;">{scheme['scheme_name']}</h3>
                    <p style="color: #94a3b8; font-size: 0.88rem; margin: 0;">🏛️ {scheme['ministry']} &nbsp;•&nbsp; {scheme['department']}</p>
                </div>
                <div>
                    {status_badge}
                </div>
            </div>
            <div style="background: #0b132b; border-left: 4px solid #4895ef; padding: 12px 16px; border-radius: 8px; margin: 14px 0; font-size: 0.93rem; color: #e2e8f0;">
                <b>🎁 Benefits:</b> {scheme['benefits']}
            </div>
        </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if res.is_eligible:
            st.success("Rule Status: PASS ✅")
        else:
            st.error("Rule Status: FAIL ❌")
    with c2:
        st.info(f"Docs Required: {len(scheme.get('required_documents', []))}")
    with c3:
        st.warning(f"Deadline: {dl['label']}")
    with c4:
        if readiness:
            st.metric("Readiness Score", f"{readiness.overall_score}%")

    with st.expander(f"🔍 View Line-by-Line Rule Evaluation for {scheme['scheme_name']}"):
        st.markdown("#### ⚖️ Deterministic Rule Engine Audit")
        
        # Rule breakdown table
        rule_cols = st.columns([2, 2, 2, 1])
        rule_cols[0].markdown("**Condition Field**")
        rule_cols[1].markdown("**Citizen Profile**")
        rule_cols[2].markdown("**Required Rule**")
        rule_cols[3].markdown("**Status**")

        for ev in res.evaluations:
            r_c1, r_c2, r_c3, r_c4 = st.columns([2, 2, 2, 1])
            r_c1.write(ev.label)
            r_c2.write(str(ev.current_value))
            r_c3.write(f"{ev.operator} {ev.required_value}")
            if ev.passed:
                r_c4.markdown("<span style='color: #4ade80; font-weight: 800;'>PASS ✅</span>", unsafe_allow_html=True)
            else:
                r_c4.markdown("<span style='color: #fca5a5; font-weight: 800;'>FAIL ❌</span>", unsafe_allow_html=True)
                st.caption(f"⚠️ {ev.failure_reason}")

        st.markdown("---")
        st.markdown("#### 📑 Required Document Checklist")
        if readiness:
            st.write(f"**Available**: `{readiness.ready_docs_count}` / `{readiness.total_docs_required}` mandatory documents")
            if readiness.missing_docs:
                st.warning(f"Missing Documents: {', '.join([d['name'] for d in readiness.missing_docs])}")
            else:
                st.success("All required documents are marked ready in your repository!")

        st.markdown("---")
        col_act1, col_act2 = st.columns(2)
        with col_act1:
            st.markdown(f"[🔗 Official Verification Portal]({scheme['official_source_url']})")
            st.caption(f"Source Last Updated: {scheme.get('last_updated', '2026-08-01')}")
        with col_act2:
            st.link_button("🌐 Apply on Official Portal", scheme['application_url'], type="primary", use_container_width=True)

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
