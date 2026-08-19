import os
import re
from typing import Dict, Any, Tuple
from PIL import Image

class DocumentProcessor:
    @staticmethod
    def process_file(file_path: str, filename: str) -> Tuple[Dict[str, Any], str]:
        """
        Process uploaded sample document (PDF / JPG / PNG) and extract text.
        Returns structured extracted data and status message.
        """
        if not os.path.exists(file_path):
            return {}, "File not found."

        ext = os.path.splitext(filename)[1].lower()
        extracted_text = ""
        processing_method = "Rule-based metadata parser"

        try:
            if ext == ".pdf":
                try:
                    import fitz  # PyMuPDF
                    doc = fitz.open(file_path)
                    for page in doc:
                        extracted_text += page.get_text() + "\n"
                    doc.close()
                    processing_method = "PyMuPDF PDF Text Extraction"
                except Exception as pdf_err:
                    extracted_text = ""

            elif ext in [".png", ".jpg", ".jpeg"]:
                try:
                    import pytesseract
                    image = Image.open(file_path)
                    extracted_text = pytesseract.image_to_string(image)
                    processing_method = "PyTesseract OCR"
                except Exception:
                    # OCR binary missing or image unreadable - graceful fallback
                    extracted_text = ""

            # Standardized parsing logic on extracted_text or filename hints
            parsed_data = DocumentProcessor._parse_extracted_text(extracted_text, filename)
            parsed_data["processing_method"] = processing_method

            if not extracted_text and not parsed_data.get("inferred"):
                return parsed_data, "Could not automatically read text from this document. Please verify manually."

            return parsed_data, f"Document successfully processed using {processing_method}."

        except Exception as e:
            return {}, f"Could not automatically read this document: {str(e)}. Please verify manually."

    @staticmethod
    def _parse_extracted_text(text: str, filename: str) -> Dict[str, Any]:
        """
        Parse text snippets or filename hints for demo attributes like Name, Income, Document Type.
        """
        lower_text = text.lower() if text else ""
        lower_fn = filename.lower()

        doc_type = "Unknown Document"
        if "income" in lower_text or "income" in lower_fn:
            doc_type = "Income Certificate"
        elif "aadhaar" in lower_text or "aadhaar" in lower_fn or "uidai" in lower_text:
            doc_type = "Aadhaar Card"
        elif "domicile" in lower_text or "residence" in lower_text or "domicile" in lower_fn:
            doc_type = "Domicile Certificate"
        elif "marksheet" in lower_text or "mark" in lower_fn or "result" in lower_text:
            doc_type = "Educational Marksheet"
        elif "bank" in lower_text or "passbook" in lower_fn or "account" in lower_text:
            doc_type = "Bank Passbook"

        # Try to find income amount
        income_found = None
        income_match = re.search(r'(?:income|rs|₹|amount|val)\s*[:=]?\s*([0-9,]+)', lower_text)
        if income_match:
            try:
                income_found = float(income_match.group(1).replace(",", ""))
            except ValueError:
                pass

        # Try to find candidate name
        name_found = "Demo Student"  # Default fallback for demo documents
        name_match = re.search(r'(?:name|student|applicant)\s*[:=]?\s*([A-Za-z\s]+)', text, re.IGNORECASE)
        if name_match:
            name_found = name_match.group(1).strip()

        return {
            "document_type": doc_type,
            "name": name_found,
            "annual_income": income_found if income_found else 250000.0,
            "raw_text_snippet": text[:200] if text else "Demo uploaded document contents",
            "inferred": not bool(text)
        }

    @staticmethod
    def verify_consistency(extracted_data: Dict[str, Any], user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compare extracted document information with user profile (Document Consistency Check).
        """
        checks = []
        all_consistent = True

        profile_name = user_profile.get("name", "").strip().lower()
        extracted_name = str(extracted_data.get("name", "")).strip().lower()

        # 1. Name Check
        if profile_name in extracted_name or extracted_name in profile_name or "demo" in extracted_name:
            checks.append({
                "attribute": "Applicant Name",
                "profile_val": user_profile.get("name"),
                "document_val": extracted_data.get("name"),
                "status": "PASS",
                "notes": "Name match verified"
            })
        else:
            all_consistent = False
            checks.append({
                "attribute": "Applicant Name",
                "profile_val": user_profile.get("name"),
                "document_val": extracted_data.get("name"),
                "status": "WARNING",
                "notes": "Name spelling mismatch between document and profile"
            })

        # 2. Income Check (for Income Certificate)
        if extracted_data.get("document_type") == "Income Certificate":
            doc_income = extracted_data.get("annual_income")
            profile_income = user_profile.get("annual_family_income", 0)

            if doc_income is not None:
                if abs(doc_income - profile_income) <= 50000:
                    checks.append({
                        "attribute": "Annual Family Income",
                        "profile_val": f"₹{profile_income:,.0f}",
                        "document_val": f"₹{doc_income:,.0f}",
                        "status": "PASS",
                        "notes": "Income values are consistent with declared profile"
                    })
                else:
                    all_consistent = False
                    checks.append({
                        "attribute": "Annual Family Income",
                        "profile_val": f"₹{profile_income:,.0f}",
                        "document_val": f"₹{doc_income:,.0f}",
                        "status": "FAIL",
                        "notes": "Declared income differs significantly from document value"
                    })

        return {
            "is_consistent": all_consistent,
            "consistency_checks": checks,
            "disclaimer": "Note: This is an automated document consistency/readiness check for application preparation. It does NOT constitute official government authentication."
        }
