# SchemeReady — Citizen Benefit Readiness Platform

> **Tagline**: *"Know your benefit. Prove your eligibility. Get application-ready."*
>
> **SIH Core Principle**: *"AI explains, rules decide."* Eligibility criteria are evaluated using a 100% deterministic Python Rule Engine. AI serves purely as an optional explanatory assistant.

---

## 📌 Project Overview

**SchemeReady** is an application readiness engine designed for citizens to bridge the gap between knowing a government scheme exists and becoming fully application-ready.

Instead of operating as a generic search portal or unstructured chatbot, SchemeReady implements a structured 6-step workflow:
1. **Citizen Profile Engine**: Captures demographic details (Age, Domicile, Income, Education).
2. **Deterministic Rule Engine**: Line-by-line evaluation of official scheme criteria (`>=`, `<=`, `==`, `in`).
3. **Smart Document Checklist**: Live readiness breakdown of mandatory vs missing documents.
4. **Document Consistency & Extraction**: Upload sample documents (PDF/PNG/JPG), extract values via PyMuPDF/OCR, and cross-verify with citizen profile.
5. **Application Readiness Score**: Deterministic readiness score formula ($50\%$ Eligibility Weight + $50\%$ Document Readiness Weight).
6. **Dynamic Deadlines, Renewals & Document Reuse**: Track real-time deadline countdowns and discover other schemes that can be unlocked using your existing documents.

---

## 🛠️ Technology Stack

- **Primary Language**: Python 3.11+
- **Frontend / UI Framework**: Streamlit
- **Database & ORM**: SQLite (`schemeready.db`), SQLAlchemy 2.0+
- **Data Validation & Parsing**: Pydantic v2, Pandas
- **Document Processing & OCR**: PyMuPDF (`fitz`), Pillow (`PIL`), PyTesseract (with graceful fallback if tesseract binary is omitted)
- **Optional AI Assistant**: Google Gemini API (`google-genai`) with offline local RAG fallback
- **Testing**: Pytest

---

## 🚀 Quickstart Guide for Beginners

### Prerequisites
- Python 3.11 or newer installed on Windows/macOS/Linux.

### 1. Clone & Navigate to Project Directory
```bash
cd C:\Users\adity\.gemini\antigravity\scratch\schemeready
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Initialize & Seed Database
```bash
python database/seed_data.py
```
*(Creates `schemeready.db` SQLite database with 6 official student/scholarship schemes and pre-loads Demo Student profile).*

### 4. Run the Streamlit Application
```bash
streamlit run app.py
```
The application will open automatically in your browser at `http://localhost:8501`.

---

## 🎬 1-Click SIH Presentation Demo Scenario

To demonstrate the full end-to-end workflow during SIH judging:

1. Open **SchemeReady** at `http://localhost:8501`.
2. Click **"🚀 Start SIH Demo Flow"** on the Home Dashboard.
3. Observe **Demo Student** profile (Age: 19, State: Uttar Pradesh, B.Tech, Income: ₹2,50,000).
4. Click **"Find Benefits For Me"** -> See **UP Post-Matric Scholarship** evaluated as **ELIGIBLE ✅**.
5. Click **Inspect Rule Breakdown** -> Verify all rules (*Age >= 16*, *Income <= 2,50,000*, *Domicile UP*) passing.
6. Notice Document Readiness starts at **4/5 (80% Readiness Score)** with **Income Certificate MISSING**.
7. Navigate to **Document Readiness** -> Upload a sample Income Certificate PDF/Image.
8. Click **Process & Extract Document Data** -> View extracted income data & profile consistency pass status.
9. Return to **Application Readiness Score** -> Watch readiness score update from **80% to 100%**!
10. Click **"Apply on Official Portal"** -> Route directly to verified government URL (`https://scholarship.up.gov.in`).

---

## 🧪 Running Automated Tests

Run the Pytest suite to verify rule evaluation logic, readiness calculations, deadline countdowns, and document reuse:

```bash
pytest tests/
```

---

## 🛡️ Data Safety & Privacy Rules

- **Sample Documents Only**: The demo environment uses dummy files for testing. Real Aadhaar or sensitive government ID numbers are never requested or saved.
- **Official Government Sources**: Scheme rules are based on verified official portals (NSP, UP Scholarship Portal, AICTE, PM YASASVI). See [`data/README_DATA_SOURCES.md`](file:///C:/Users/adity/.gemini/antigravity/scratch/schemeready/data/README_DATA_SOURCES.md) for source links.
