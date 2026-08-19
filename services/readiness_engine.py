from typing import Dict, Any, List
from dataclasses import dataclass, field

@dataclass
class ReadinessResult:
    scheme_id: str
    scheme_name: str
    eligibility_score: float  # 0.0 to 50.0
    document_score: float     # 0.0 to 50.0
    overall_score: float      # 0.0 to 100.0
    total_docs_required: int
    ready_docs_count: int
    missing_docs: List[Dict[str, str]] = field(default_factory=list)
    ready_docs: List[Dict[str, str]] = field(default_factory=list)
    next_action: str = ""

class ReadinessEngine:
    @staticmethod
    def calculate_readiness(
        is_eligible: bool,
        required_documents: List[Dict[str, Any]],
        user_documents: List[Dict[str, Any]]
    ) -> ReadinessResult:
        """
        Deterministic Readiness Score Formula:
        Overall Readiness Score = Eligibility Weight (50%) + Document Weight (50%)

        If Eligible: Eligibility Score = 50.0 else 0.0
        Document Score = (Ready Mandatory Documents / Total Mandatory Documents) * 50.0
        """
        eligibility_score = 50.0 if is_eligible else 0.0

        # Map available user document doc_ids
        available_doc_ids = {
            doc.get("doc_id") for doc in user_documents 
            if doc.get("status") in ["Available", "Verified", "READY", "Ready"]
        }

        total_docs = len(required_documents)
        ready_docs = []
        missing_docs = []

        if total_docs == 0:
            doc_score = 50.0
            ready_count = 0
        else:
            ready_count = 0
            for req_doc in required_documents:
                doc_id = req_doc.get("doc_id")
                doc_name = req_doc.get("name", doc_id)
                
                if doc_id in available_doc_ids:
                    ready_count += 1
                    ready_docs.append({"doc_id": doc_id, "name": doc_name})
                else:
                    missing_docs.append({
                        "doc_id": doc_id, 
                        "name": doc_name,
                        "description": req_doc.get("description", "")
                    })

            doc_score = (ready_count / total_docs) * 50.0

        overall_score = round(eligibility_score + doc_score, 1)

        # Determine next actionable advice
        if not is_eligible:
            next_action = "Review eligibility criteria and update profile if information was incorrect."
        elif missing_docs:
            missing_names = ", ".join([d["name"] for d in missing_docs[:2]])
            next_action = f"Obtain and upload missing document(s): {missing_names}"
        else:
            next_action = "All criteria met & all documents ready! Proceed to apply on official portal."

        return ReadinessResult(
            scheme_id="",
            scheme_name="",
            eligibility_score=eligibility_score,
            document_score=doc_score,
            overall_score=overall_score,
            total_docs_required=total_docs,
            ready_docs_count=ready_count,
            missing_docs=missing_docs,
            ready_docs=ready_docs,
            next_action=next_action
        )
