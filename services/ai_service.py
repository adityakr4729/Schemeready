import os
import re
from typing import List, Dict, Any, Optional
from services.eligibility_engine import RuleEngine
from services.deadline_service import DeadlineService

class AIService:
    @staticmethod
    def is_ai_available() -> bool:
        """Check if Gemini API key is configured."""
        key = os.environ.get("GEMINI_API_KEY", "").strip()
        return bool(key and key != "your_gemini_api_key_here")

    @staticmethod
    def answer_question(
        query: str, 
        user_profile: Dict[str, Any], 
        schemes_data: List[Dict[str, Any]],
        language: str = "English",
        user_docs: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Answer user questions safely using local scheme context (RAG) or Gemini API if present.
        Supports English, Hindi, and Hinglish automatically.
        """
        api_available = AIService.is_ai_available()
        q_lower = query.lower().strip()

        # Auto-detect Hindi / Hinglish in query
        hindi_keywords = ["kaun", "konsi", "kon", "kya", "kab", "kaise", "chahiye", "milegi", "miloge", "dastavej", "yojana", "hindi", "batao", "mujhe", "mera", "meri", "aavedan", "scolarship", "sholarship"]
        is_hindi_query = language in ["Hindi", "Hinglish"] or any(k in q_lower for k in hindi_keywords) or any("\u0900" <= c <= "\u097f" for c in query)

        # Build local context summary of schemes
        scheme_summaries = []
        for s in schemes_data:
            summary = (
                f"Scheme Name: {s.get('scheme_name')}\n"
                f"Ministry: {s.get('ministry')}\n"
                f"State: {s.get('state')}\n"
                f"Category: {s.get('category')}\n"
                f"Benefits: {s.get('benefits')}\n"
                f"Deadline: {s.get('deadline')}\n"
                f"Renewal Info: {s.get('renewal_information')}\n"
                f"URL: {s.get('official_source_url')}\n"
            )
            scheme_summaries.append(summary)
        context_text = "\n---\n".join(scheme_summaries)

        if api_available:
            try:
                from google import genai
                client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
                
                lang_instruction = "Answer in clear simple Hindi/Hinglish as requested by user." if is_hindi_query else f"Language mode: {language}"

                system_prompt = (
                    "You are SchemeReady Assistant, an official citizen benefit advisory AI. "
                    f"{lang_instruction} "
                    "Rule 1: Never invent government schemes, eligibility rules, or deadlines. "
                    "Rule 2: Base all facts strictly on the provided scheme context below. "
                    "Rule 3: If information is not in context, state clearly: 'I don't have verified information for this question.' "
                    "Rule 4: State clearly that final eligibility is decided by the rule engine, not AI."
                )
                
                user_prompt = f"User Profile: {user_profile}\nContext Schemes:\n{context_text}\n\nUser Question: {query}"
                
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[system_prompt, user_prompt]
                )
                return {
                    "answer": response.text,
                    "source": "Official scheme database (verified by Gemini AI)",
                    "mode": "Gemini AI"
                }
            except Exception:
                # Fallback to local rule-based answer if API call encounters network error
                pass

        # Fallback Local Rule RAG Engine
        return AIService._local_fallback_answer(query, user_profile, schemes_data, language, user_docs, is_hindi_query)

    @staticmethod
    def _local_fallback_answer(
        query: str, 
        user_profile: Dict[str, Any], 
        schemes_data: List[Dict[str, Any]],
        language: str = "English",
        user_docs: List[Dict[str, Any]] = None,
        is_hindi: bool = False
    ) -> Dict[str, Any]:
        """
        Comprehensive Local RAG Engine supporting English & Hindi/Hinglish.
        """
        q_lower = query.lower()
        user_docs = user_docs or []
        available_doc_ids = {d["doc_id"] for d in user_docs if d.get("status") in ["Available", "Verified", "READY", "Ready"]}

        # 1. Eligibility / Suited Schemes Query
        if any(w in q_lower for w in ["suit", "eligible", "qualify", "which scheme", "my scheme", "for me", "kaun", "konsi", "milegi", "yojana"]):
            eligible_schemes = []
            for s in schemes_data:
                res = RuleEngine.evaluate_scheme(user_profile, s)
                if res.is_eligible:
                    eligible_schemes.append(s)

            if eligible_schemes:
                scheme_list_str = "\n".join([
                    f"- **{s['scheme_name']}** ({s['category']}): {s['benefits']} | Deadline: {s.get('deadline', 'N/A')}" 
                    for s in eligible_schemes
                ])
                if is_hindi:
                    ans = (
                        f"Aapke citizen profile (Umar: **{user_profile.get('age')} years**, State: **{user_profile.get('state')}**, Income: **₹{user_profile.get('annual_family_income'):,.0f}**) "
                        f"ke aadhar par aap **{len(eligible_schemes)} sarkari yojanaon (schemes)** ke liye 100% eligible hain:\n\n"
                        f"{scheme_list_str}\n\n"
                        f"💡 **Tip**: Aap 'Find Benefits For Me' tab me sabhi eligibility rules ki line-by-line verification dekh sakte hain."
                    )
                else:
                    ans = (
                        f"Based on your profile (Age: **{user_profile.get('age')}**, State: **{user_profile.get('state')}**, Annual Income: **₹{user_profile.get('annual_family_income'):,.0f}**), "
                        f"you satisfy all rule conditions for **{len(eligible_schemes)} schemes**:\n\n"
                        f"{scheme_list_str}\n\n"
                        f"*Note: Final eligibility is determined line-by-line by our deterministic Rule Engine.*"
                    )
            else:
                if is_hindi:
                    ans = "Aapke bataye gaye profile ke aadhar par abhi koi scheme match nahi ho rahi hai. Kripya apna Profile tab me Annual Family Income ya State details verify karein."
                else:
                    ans = "Based on your current profile, no schemes match 100% of rule requirements. Please review your declared income or state of domicile in the Profile tab."

        # 2. Missing Documents Query
        elif any(w in q_lower for w in ["missing", "document", "proof", "need", "checklist", "required", "dastavej", "dastavez", "kaunse"]):
            all_req_docs = {}
            for s in schemes_data:
                for d in s.get("required_documents", []):
                    all_req_docs[d["doc_id"]] = d["name"]

            missing_list = [name for doc_id, name in all_req_docs.items() if doc_id not in available_doc_ids]
            ready_list = [name for doc_id, name in all_req_docs.items() if doc_id in available_doc_ids]

            if is_hindi:
                if missing_list:
                    ans = (
                        f"📑 **Document Readiness Status**:\n\n"
                        f"✅ **Taiyaar Dastavez ({len(ready_list)})**: {', '.join(ready_list) if ready_list else 'Koyi nahi'}\n\n"
                        f"🔴 **Baki Dastavez ({len(missing_list)})**: {', '.join(missing_list)}\n\n"
                        f"💡 **Aage Kya Karein**: Application readiness ko 100% karne ke liye **Document Readiness** tab me missing documents upload ya mark karein."
                    )
                else:
                    ans = "🎉 **Aapke sabhi zaroori dastavez ready hain!** (Aadhaar Card, Income Certificate, Domicile, Marksheet, Bank Passbook)."
            else:
                if missing_list:
                    ans = (
                        f"📑 **Document Readiness Summary**:\n\n"
                        f"✅ **Ready Documents ({len(ready_list)})**: {', '.join(ready_list) if ready_list else 'None'}\n\n"
                        f"🔴 **Missing Documents ({len(missing_list)})**: {', '.join(missing_list)}\n\n"
                        f"💡 **Action Required**: Please upload or mark your missing documents in the **Document Readiness** tab to reach 100% application readiness."
                    )
                else:
                    ans = "🎉 **All required documents are READY!** You possess all mandatory certificates (Aadhaar, Income Certificate, Domicile, Marksheet, Bank Passbook)."

        # 3. Deadlines Query
        elif any(w in q_lower for w in ["deadline", "last date", "when", "date", "expire", "time", "kab"]):
            dl_lines = []
            for s in schemes_data:
                dl_info = DeadlineService.get_deadline_status(s.get("deadline"))
                dl_lines.append(f"- **{s['scheme_name']}**: {dl_info['label']} (Date: {dl_info['deadline_date'] or 'N/A'})")
            
            if is_hindi:
                ans = "⏳ **Scheme Application ki Last Dates (Deadlines)**:\n\n" + "\n".join(dl_lines)
            else:
                ans = "⏳ **Verified Application Deadlines**:\n\n" + "\n".join(dl_lines)

        # 4. Renewal Query
        elif any(w in q_lower for w in ["renew", "renewal", "continue", "next year", "dobaara"]):
            ren_lines = []
            for s in schemes_data:
                ren_info = DeadlineService.get_renewal_status(s)
                status_str = "Renewal Zaroori Hai" if ren_info['renewal_required'] else "Renewal Zaroori Nahi"
                ren_lines.append(f"- **{s['scheme_name']}**: {status_str} — *{ren_info['information']}*")
            
            if is_hindi:
                ans = "🔄 **Scheme Renewal ki Jankari**:\n\n" + "\n".join(ren_lines)
            else:
                ans = "🔄 **Scheme Renewal Information**:\n\n" + "\n".join(ren_lines)

        # 5. General / Default Answer
        else:
            if is_hindi:
                ans = (
                    f"Main SchemeReady AI Assistant hoon. Main aapke inse jude sawaalon ke jawab de sakta hoon:\n"
                    f"1. *Mujhe kaun si yojana milegi?* (Which schemes suit me?)\n"
                    f"2. *Konse documents missing hain?* (Which documents am I missing?)\n"
                    f"3. *Last date kab hai?* (When are scheme deadlines?)\n"
                    f"4. *Renewal kaise hoga?* (What are the renewal criteria?)"
                )
            else:
                ans = (
                    f"I found {len(schemes_data)} official schemes in the database. "
                    f"You can ask me about:\n"
                    f"1. *Which schemes suit me?*\n"
                    f"2. *Which documents am I missing?*\n"
                    f"3. *When are scheme deadlines?*\n"
                    f"4. *What are the renewal criteria?*"
                )

        return {
            "answer": ans,
            "source": "Official Scheme Database (Deterministic RAG Engine)",
            "mode": "Offline Local RAG"
        }
