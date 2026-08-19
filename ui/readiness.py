import streamlit as st
from services.readiness_engine import ReadinessResult

def render_readiness_page(readiness_results: list, all_schemes: list):
    st.markdown("""
        <div style="background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%); padding: 25px; border-radius: 16px; color: white; margin-bottom: 25px; box-shadow: 0 10px 25px rgba(2,132,199,0.2);">
            <h2 style="margin: 0; font-weight: 800;">📊 Application Readiness Engine</h2>
            <p style="font-size: 1rem; opacity: 0.9; margin-top: 5px;">Transparent, non-arbitrary mathematical readiness calculation.</p>
        </div>
    """, unsafe_allow_html=True)

    if not readiness_results:
        st.info("No readiness data available. Please check your citizen profile.")
        return

    # Select scheme to inspect
    scheme_options = {r.scheme_id: r.scheme_name for r in readiness_results}
    selected_scheme_id = st.selectbox(
        "Select Scheme to Inspect Application Readiness",
        options=list(scheme_options.keys()),
        format_func=lambda x: f"{x} - {scheme_options[x]}"
    )

    # Find selected result
    res: ReadinessResult = next((r for r in readiness_results if r.scheme_id == selected_scheme_id), readiness_results[0])
    target_scheme = next((s for s in all_schemes if s["scheme_id"] == res.scheme_id), {})

    score_color = '#16a34a' if res.overall_score >= 90 else '#d97706' if res.overall_score >= 50 else '#dc2626'

    # Readiness Score Dashboard Header Card
    st.markdown(f"""
        <div style="border: 2px solid #3b82f6; border-radius: 16px; padding: 28px; background: #ffffff; margin-bottom: 25px; box-shadow: 0 10px 30px rgba(59,130,246,0.08);">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="background: #eff6ff; color: #1d4ed8; padding: 4px 12px; border-radius: 9999px; font-weight: 700; font-size: 0.8rem;">MATHEMATICAL FORMULA</span>
                    <h2 style="color: #0f172a; margin: 8px 0 2px 0; font-weight: 800;">APPLICATION READINESS SCORE</h2>
                    <h4 style="color: #64748b; margin: 0; font-weight: 600;">{res.scheme_name}</h4>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 4rem; font-weight: 800; color: {score_color}; line-height: 1;">
                        {res.overall_score}%
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Progress Bar
    st.progress(res.overall_score / 100.0)

    # Formula Transparency Box
    with st.expander("🧮 How is this score calculated? (Transparent Formula)"):
        st.markdown(f"""
            **Deterministic Readiness Formula**:
            $$\\text{{Overall Score}} = \\text{{Eligibility Weight (50\\%)}} + \\text{{Document Readiness Weight (50\\%)}}$$

            - **Eligibility Score**: `{res.eligibility_score} / 50.0` ({'Full Marks for Eligibility' if res.eligibility_score == 50.0 else 'Ineligible Profile'})
            - **Document Score**: `{res.document_score} / 50.0` (`{res.ready_docs_count}` of `{res.total_docs_required}` mandatory documents ready)
            - **Total Score**: `{res.overall_score}%`
        """)

    st.markdown("<hr style='margin: 25px 0; border-color: #e2e8f0;'>", unsafe_allow_html=True)

    # Major Feature: WHAT AM I MISSING?
    st.markdown("### ❓ WHAT AM I MISSING?")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
            <div style="background-color: {'#f0fdf4' if res.eligibility_score == 50.0 else '#fef2f2'}; border-left: 5px solid {'#16a34a' if res.eligibility_score == 50.0 else '#dc2626'}; padding: 18px; border-radius: 12px; height: 100%;">
                <h4 style="margin:0; color: {'#15803d' if res.eligibility_score == 50.0 else '#b91c1c'}; font-weight: 700;">1. Rule Eligibility</h4>
                <p style="font-size: 1.05rem; margin-top: 6px; color: #334155; font-weight: 600;">
                    {'Complete ✅ All eligibility criteria passed' if res.eligibility_score == 50.0 else 'Incomplete ❌ Profile fails scheme criteria'}
                </p>
            </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
            <div style="background-color: {'#f0fdf4' if res.ready_docs_count == res.total_docs_required else '#fffbeb'}; border-left: 5px solid {'#16a34a' if res.ready_docs_count == res.total_docs_required else '#d97706'}; padding: 18px; border-radius: 12px; height: 100%;">
                <h4 style="margin:0; color: {'#15803d' if res.ready_docs_count == res.total_docs_required else '#b45309'}; font-weight: 700;">2. Document Readiness</h4>
                <p style="font-size: 1.05rem; margin-top: 6px; color: #334155; font-weight: 600;">
                    <b>{res.ready_docs_count} / {res.total_docs_required}</b> documents ready ({int((res.ready_docs_count/res.total_docs_required)*100) if res.total_docs_required>0 else 100}%)
                </p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    st.markdown("#### 🚨 Missing Documents & Actionable Next Steps")
    if not res.missing_docs:
        st.success("🎉 You are 100% Application Ready! No missing documents. Click below to apply on official portal.")
        st.link_button("🌐 Apply on Official Government Portal", target_scheme.get("application_url", "https://scholarships.gov.in"), type="primary", use_container_width=True)
    else:
        st.error(f"You have **{len(res.missing_docs)} missing document(s)** preventing 100% readiness:")
        for doc in res.missing_docs:
            st.markdown(f"- 🔴 **{doc['name']}**: {doc.get('description', 'Required certificate for validation')}")

        st.info(f"💡 **Recommended Next Step**: {res.next_action}")
