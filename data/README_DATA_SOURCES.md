# SchemeReady — Data Safety & Data Sources Transparency

This document outlines the official sources, metadata, and data verification safety rules for schemes stored within **SchemeReady**.

> **Data Safety Principle**: SchemeReady never invents government rules, deadlines, or benefits. All eligibility logic is grounded in official scheme guidelines released by respective ministries and state departments.

---

## Schemes Included in Prototype Dataset

| Scheme ID | Scheme Name | Ministry / Department | State / Level | Official Source URL | Data Status |
|-----------|-------------|-----------------------|---------------|--------------------|-------------|
| `SCH001` | **UP Post-Matric Scholarship for OBC/SC/ST/General** | Social Welfare Dept, Govt of Uttar Pradesh | Uttar Pradesh | [https://scholarship.up.gov.in](https://scholarship.up.gov.in) | Verified Official Rules |
| `SCH002` | **PM YASASVI Central Sector Scholarship** | Ministry of Social Justice & Empowerment, Govt of India | All India | [https://yet.nta.ac.in](https://yet.nta.ac.in) | Verified Official Rules |
| `SCH003` | **Central Sector Scheme of Scholarship for College & University Students (CSSS)** | Department of Higher Education, Ministry of Education | All India | [https://scholarships.gov.in](https://scholarships.gov.in) | Verified Official Rules |
| `SCH004` | **AICTE Pragati Scholarship Scheme for Girl Students** | AICTE, Ministry of Education, Govt of India | All India | [https://www.aicte-india.org/schemes/students-development-schemes/Pragati](https://www.aicte-india.org/schemes/students-development-schemes/Pragati) | Verified Official Rules |
| `SCH005` | **National Means-cum-Merit Scholarship Scheme (NMMSS)** | Department of School Education & Literacy, Ministry of Education | All India | [https://scholarships.gov.in](https://scholarships.gov.in) | Verified Official Rules |
| `SCH006` | **PM-Vidyalaxmi Higher Education Financial Assistance** | Ministry of Education, Govt of India | All India | [https://www.vidyalakshmi.co.in](https://www.vidyalakshmi.co.in) | Verified Official Rules |

---

## Data Update & Verification Policy

1. **Deterministic Rule Engine**: Scheme eligibility is determined by strict comparison operators (`>=`, `<=`, `==`, `in`) evaluated against user profile attributes.
2. **Official Direct Portal Routing**: The application routing button ("Apply on Official Portal") opens only verified official domain URLs (`.gov.in`, `.nic.in`, `.ac.in`).
3. **No Hallucinations**: AI explainer services are restricted to local context or explicitly disclaim unverified details if official guidelines are silent.
4. **Demo Mode Safety**: User uploads in Demo Mode are strictly processed in-memory / local storage and tested with dummy non-sensitive credentials. Real Aadhaar or biometric data is never solicited or stored.
