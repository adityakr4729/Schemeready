import os
import streamlit as st
from sqlalchemy.orm import Session
from database.models import UserDocument
from services.document_processor import DocumentProcessor

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")

def render_documents_page(db: Session, user_profile: dict, user_docs: list):
    st.markdown("""
        <div style="background: linear-gradient(135deg, #059669 0%, #047857 100%); padding: 25px; border-radius: 16px; color: white; margin-bottom: 25px; box-shadow: 0 10px 25px rgba(5,150,105,0.2);">
            <h2 style="margin: 0; font-weight: 800;">📄 Smart Document Readiness & Consistency Check</h2>
            <p style="font-size: 1rem; opacity: 0.9; margin-top: 5px;">Manage document availability, upload sample proofs, extract structured data, and verify profile consistency.</p>
        </div>
    """, unsafe_allow_html=True)

    st.warning("⚠️ **SIH Demo Notice**: Use sample/demo documents for testing. Do NOT upload real Aadhaar numbers or sensitive personal documents.")

    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Required Document Catalog for UI
    all_doc_types = [
        {"doc_id": "DOC_AADHAAR", "name": "Aadhaar Card", "desc": "Government identity verification"},
        {"doc_id": "DOC_INCOME", "name": "Income Certificate", "desc": "Family income proof"},
        {"doc_id": "DOC_DOMICILE", "name": "Domicile Certificate", "desc": "State residence proof"},
        {"doc_id": "DOC_MARKSHEET", "name": "Educational Marksheet", "desc": "Qualifying marksheet"},
        {"doc_id": "DOC_BANK", "name": "Bank Passbook", "desc": "Direct Benefit Transfer (DBT) details"},
    ]

    user_doc_map = {d["doc_id"]: d for d in user_docs}

    st.markdown("### 📋 Document Status Checklist")

    checklist_cols = st.columns([2, 3, 2, 2])
    checklist_cols[0].markdown("**Document Name**")
    checklist_cols[1].markdown("**Description**")
    checklist_cols[2].markdown("**Status**")
    checklist_cols[3].markdown("**Action**")

    for doc_item in all_doc_types:
        d_id = doc_item["doc_id"]
        d_name = doc_item.get("name", doc_item.get("doc_name", d_id))
        d_desc = doc_item["desc"]

        existing_doc = user_doc_map.get(d_id)
        current_status = existing_doc["status"] if existing_doc else "Missing"

        c1, c2, c3, c4 = st.columns([2, 3, 2, 2])
        c1.write(f"**{d_name}**")
        c2.write(d_desc)

        if current_status in ["Available", "Verified", "READY", "Ready"]:
            c3.markdown("<span style='color: #16a34a; font-weight: 800;'>READY ✅</span>", unsafe_allow_html=True)
        else:
            c3.markdown("<span style='color: #dc2626; font-weight: 800;'>MISSING ❌</span>", unsafe_allow_html=True)

        # Toggle status button
        if current_status in ["Available", "Verified", "READY", "Ready"]:
            if c4.button(f"Mark Missing", key=f"btn_miss_{d_id}", use_container_width=True):
                _update_doc_status(db, user_profile["id"], d_id, d_name, "Missing")
                st.rerun()
        else:
            if c4.button(f"Mark Available", key=f"btn_avail_{d_id}", use_container_width=True):
                _update_doc_status(db, user_profile["id"], d_id, d_name, "Available")
                st.rerun()

    st.markdown("<hr style='margin: 30px 0; border-color: #e2e8f0;'>", unsafe_allow_html=True)
    st.markdown("### 📤 Sample Document Upload & Automated OCR Verification")

    doc_to_upload = st.selectbox(
        "Select Document Type to Upload",
        [
            ("DOC_INCOME", "Income Certificate (Demo Scenario Upload)"),
            ("DOC_AADHAAR", "Aadhaar Card"),
            ("DOC_DOMICILE", "Domicile Certificate"),
            ("DOC_MARKSHEET", "Educational Marksheet"),
            ("DOC_BANK", "Bank Passbook")
        ],
        format_func=lambda x: x[1]
    )

    uploaded_file = st.file_uploader(
        "Upload Sample Document (PDF, PNG, JPG, JPEG)",
        type=["pdf", "png", "jpg", "jpeg"]
    )

    if uploaded_file is not None:
        if st.button("⚡ Process & Extract Document Data", type="primary", use_container_width=True):
            target_doc_id = doc_to_upload[0]
            target_doc_name = doc_to_upload[1].split(" (")[0]

            file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.info(f"File saved to local sandbox: `{uploaded_file.name}`. Running Document Processor...")

            # Run Document Processor OCR
            extracted_data, msg = DocumentProcessor.process_file(file_path, uploaded_file.name)
            
            # Set target document type explicitly for verification if needed
            extracted_data["document_type"] = target_doc_name

            st.success(msg)

            st.markdown("#### 🤖 Extracted Data Snippet")
            st.json(extracted_data)

            # Run Document Consistency Checker
            st.markdown("#### ⚖️ Document Consistency Check vs Citizen Profile")
            consistency_result = DocumentProcessor.verify_consistency(extracted_data, user_profile)
            
            st.write(f"**Overall Consistency Status**: {'PASS ✅' if consistency_result['is_consistent'] else 'ATTENTION REQUIRED ⚠️'}")

            for chk in consistency_result["consistency_checks"]:
                st.write(f"- **{chk['attribute']}**: Profile=`{chk['profile_val']}` | Document=`{chk['document_val']}` -> **{chk['status']}** ({chk['notes']})")

            st.caption(consistency_result["disclaimer"])

            # Update DB state to Available
            _update_doc_status(db, user_profile["id"], target_doc_id, target_doc_name, "Available", file_path, extracted_data, "Verified via Document Processor")
            st.success(f"Updated '{target_doc_name}' status to AVAILABLE! Readiness score recalculating...")
            st.rerun()

def _update_doc_status(db: Session, user_id: int, doc_id: str, doc_name: str, status: str, file_path=None, extracted_data=None, notes=None):
    user_doc = db.query(UserDocument).filter_by(user_id=user_id, doc_id=doc_id).first()
    if not user_doc:
        user_doc = UserDocument(
            user_id=user_id,
            doc_id=doc_id,
            doc_name=doc_name
        )
        db.add(user_doc)
    
    user_doc.status = status
    if file_path:
        user_doc.file_path = file_path
    if extracted_data:
        user_doc.extracted_data = extracted_data
    if notes:
        user_doc.verification_notes = notes

    db.commit()
