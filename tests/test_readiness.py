import pytest
from services.readiness_engine import ReadinessEngine
from services.document_reuse import DocumentReuseEngine

def test_readiness_calculation_partial_docs():
    required_documents = [
        {"doc_id": "DOC_AADHAAR", "name": "Aadhaar Card"},
        {"doc_id": "DOC_INCOME", "name": "Income Certificate"},
        {"doc_id": "DOC_DOMICILE", "name": "Domicile Certificate"},
        {"doc_id": "DOC_MARKSHEET", "name": "Marksheet"},
        {"doc_id": "DOC_BANK", "name": "Bank Passbook"}
    ]

    # 4/5 documents available
    user_documents = [
        {"doc_id": "DOC_AADHAAR", "status": "Available"},
        {"doc_id": "DOC_DOMICILE", "status": "Available"},
        {"doc_id": "DOC_MARKSHEET", "status": "Available"},
        {"doc_id": "DOC_BANK", "status": "Available"}
    ]

    # Eligible user = 50% eligibility + (4/5 * 50%) = 50 + 40 = 90%
    result = ReadinessEngine.calculate_readiness(
        is_eligible=True,
        required_documents=required_documents,
        user_documents=user_documents
    )

    assert result.eligibility_score == 50.0
    assert result.document_score == 40.0
    assert result.overall_score == 90.0
    assert result.ready_docs_count == 4
    assert len(result.missing_docs) == 1
    assert result.missing_docs[0]["doc_id"] == "DOC_INCOME"

def test_document_reuse_engine():
    user_available_doc_ids = ["DOC_AADHAAR", "DOC_DOMICILE", "DOC_MARKSHEET", "DOC_BANK"]
    all_schemes = [
        {
            "scheme_id": "SCH001",
            "scheme_name": "Scheme A",
            "category": "Scholarship",
            "required_documents": [
                {"doc_id": "DOC_AADHAAR", "name": "Aadhaar"},
                {"doc_id": "DOC_DOMICILE", "name": "Domicile"},
                {"doc_id": "DOC_MARKSHEET", "name": "Marksheet"}
            ]
        }
    ]

    reuse_res = DocumentReuseEngine.analyze_document_reuse(user_available_doc_ids, all_schemes)
    assert len(reuse_res) == 1
    assert reuse_res[0]["matched_count"] == 3
    assert reuse_res[0]["total_count"] == 3
    assert reuse_res[0]["is_fully_ready"] is True
