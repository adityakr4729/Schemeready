import streamlit as st
from services.deadline_service import DeadlineService
from services.document_reuse import DocumentReuseEngine

def render_deadlines_and_reuse_page(all_schemes: list, user_available_doc_ids: list):
    st.markdown("""
        <div style="background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%); padding: 25px; border-radius: 16px; color: white; margin-bottom: 25px; box-shadow: 0 10px 25px rgba(124,58,237,0.2);">
            <h2 style="margin: 0; font-weight: 800;">⏳ Deadlines, Renewals & Document Reuse Engine</h2>
            <p style="font-size: 1rem; opacity: 0.9; margin-top: 5px;">Track application urgency, renewal requirements, and discover schemes compatible with your existing documents.</p>
        </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📅 Dynamic Deadline Tracker", "🔄 Renewal Tracker", "♻️ Cross-Scheme Document Reuse"])

    # TAB 1: DEADLINES
    with tab1:
        st.markdown("### ⏰ Real-Time Scheme Application Deadlines")
        st.caption("Days remaining calculated dynamically using Python's datetime library.")

        for s in all_schemes:
            dl_info = DeadlineService.get_deadline_status(s.get("deadline"))
            
            with st.container():
                c1, c2, c3, c4 = st.columns([3, 2, 2, 2])
                c1.markdown(f"**{s['scheme_name']}**<br><small style='color: #64748b;'>{s['ministry']}</small>", unsafe_allow_html=True)
                c2.write(f"📅 Deadline: **{dl_info['deadline_date'] or 'N/A'}**")
                
                if dl_info['status'] == "Safe":
                    c3.markdown(f"<span style='background:#dcfce7; color:#15803d; padding:6px 14px; border-radius:9999px; font-weight:bold; font-size:0.85rem;'>{dl_info['label']}</span>", unsafe_allow_html=True)
                elif dl_info['status'] == "Approaching":
                    c3.markdown(f"<span style='background:#fef3c7; color:#b45309; padding:6px 14px; border-radius:9999px; font-weight:bold; font-size:0.85rem;'>{dl_info['label']}</span>", unsafe_allow_html=True)
                elif dl_info['status'] in ["Urgent", "Expired"]:
                    c3.markdown(f"<span style='background:#fee2e2; color:#b91c1c; padding:6px 14px; border-radius:9999px; font-weight:bold; font-size:0.85rem;'>{dl_info['label']}</span>", unsafe_allow_html=True)
                else:
                    c3.write("No deadline date")

                c4.link_button("Official Portal", s["application_url"], use_container_width=True)
                st.markdown("<hr style='margin: 12px 0; border-color: #f1f5f9;'>", unsafe_allow_html=True)

    # TAB 2: RENEWALS
    with tab2:
        st.markdown("### 🔄 Annual Scheme Renewal Schedule")
        
        for s in all_schemes:
            ren_info = DeadlineService.get_renewal_status(s)
            with st.container():
                c1, c2, c3 = st.columns([3, 2, 3])
                c1.markdown(f"**{s['scheme_name']}**")
                if ren_info['renewal_required']:
                    c2.markdown("<span style='background: #e0f2fe; color: #0369a1; padding: 4px 12px; border-radius: 9999px; font-weight: 700; font-size:0.85rem;'>RENEWAL REQUIRED ✅</span>", unsafe_allow_html=True)
                else:
                    c2.markdown("<span style='color: #64748b;'>Renewal Not Required</span>", unsafe_allow_html=True)
                c3.write(ren_info['information'])
                st.markdown("<hr style='margin: 12px 0; border-color: #f1f5f9;'>", unsafe_allow_html=True)

    # TAB 3: DOCUMENT REUSE ENGINE
    with tab3:
        st.markdown("### ♻️ Document Reuse Engine (SIH Innovation)")
        st.info("💡 **Core Idea**: If you have already obtained your Aadhaar, Domicile, or Income Certificate, discover what *other* government benefits you can apply for using the exact same documents.")

        reuse_results = DocumentReuseEngine.analyze_document_reuse(user_available_doc_ids, all_schemes)

        if not reuse_results:
            st.warning("Upload or mark documents as 'Available' in the Document Readiness tab to see cross-scheme reuse potential.")
        else:
            fully_ready = sum(1 for r in reuse_results if r['is_fully_ready'])
            st.success(f"🎉 Your existing document repository contains documents needed by **{len(reuse_results)} schemes** ({fully_ready} schemes are 100% document-ready!).")

            for res in reuse_results:
                with st.container():
                    c1, c2, c3 = st.columns([3, 2, 2])
                    c1.markdown(f"**{res['scheme_name']}** ({res['category']})")
                    c2.write(f"📄 Matched Docs: **{res['matched_count']} / {res['total_count']}** ({res['match_percentage']}%)")
                    if res['is_fully_ready']:
                        c3.markdown("<span style='background:#dcfce7; color:#15803d; padding:4px 12px; border-radius:9999px; font-weight:bold; font-size:0.85rem;'>100% Document Ready!</span>", unsafe_allow_html=True)
                    else:
                        c3.warning(f"Needs: {', '.join(res['missing_docs'])}")
                    
                    st.caption(f"Reusable Documents: {', '.join(res['matched_docs'])}")
                    st.markdown("<hr style='margin: 12px 0; border-color: #f1f5f9;'>", unsafe_allow_html=True)
