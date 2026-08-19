from typing import List, Dict, Any

class DocumentReuseEngine:
    @staticmethod
    def analyze_document_reuse(
        user_available_doc_ids: List[str],
        all_schemes: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Analyze user's existing available documents against all schemes
        to show cross-scheme document reuse potential.
        """
        user_doc_set = set(user_available_doc_ids)
        reuse_results = []

        for scheme in all_schemes:
            req_docs = scheme.get("required_documents", [])
            if not req_docs:
                continue

            matched_docs = []
            missing_docs = []

            for req in req_docs:
                d_id = req.get("doc_id")
                d_name = req.get("name", d_id)
                if d_id in user_doc_set:
                    matched_docs.append(d_name)
                else:
                    missing_docs.append(d_name)

            matched_count = len(matched_docs)
            total_count = len(req_docs)
            match_percentage = round((matched_count / total_count) * 100, 1) if total_count > 0 else 100.0

            # Include scheme if at least 1 document matches
            if matched_count > 0:
                reuse_results.append({
                    "scheme_id": scheme.get("scheme_id"),
                    "scheme_name": scheme.get("scheme_name"),
                    "category": scheme.get("category"),
                    "matched_count": matched_count,
                    "total_count": total_count,
                    "match_percentage": match_percentage,
                    "matched_docs": matched_docs,
                    "missing_docs": missing_docs,
                    "is_fully_ready": matched_count == total_count
                })

        # Sort by highest match percentage and matched count
        reuse_results.sort(key=lambda x: (x["match_percentage"], x["matched_count"]), reverse=True)
        return reuse_results
