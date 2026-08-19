# SchemeReady System Constants

APP_NAME = "SchemeReady"

TAGLINE = {
    "English": "Know your benefit. Prove your eligibility. Get application-ready.",
    "Hindi": "अपनी योजना जानें। अपनी पात्रता साबित करें। आवेदन के लिए तैयार हों।",
    "Hinglish": "Apni scheme jaanein. Eligibility prove karein. Application-ready banein."
}

PROBLEM_STATEMENT = {
    "English": (
        "Citizens often know government schemes exist, but struggle to understand eligibility rules, "
        "required documents, document readiness, deadline constraints, and official application portals. "
        "SchemeReady converts official government scheme criteria into a transparent, rule-based readiness engine."
    ),
    "Hindi": (
        "नागरिकों को अक्सर पता होता है कि सरकारी योजनाएं मौजूद हैं, लेकिन वे पात्रता नियमों, आवश्यक दस्तावेजों, "
        "दस्तावेज़ तत्परता, समय सीमा और आधिकारिक आवेदन पोर्टल को समझने में असमर्थ रहते हैं। "
        "SchemeReady आधिकारिक सरकारी योजना मानदंडों को एक पारदर्शी, नियम-आधारित तत्परता इंजन में परिवर्तित करता है।"
    ),
    "Hinglish": (
        "Citizens ko pata hota hai ki sarkari schemes exist karti hain, par wo eligibility rules, required documents, "
        "document readiness, deadline constraints, aur official portals samajhne me struggle karte hain. "
        "SchemeReady official sarkari scheme criteria ko ek transparent, rule-based readiness engine me convert karta hai."
    )
}

STATES_LIST = [
    "All India",
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
    "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram",
    "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
    "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal",
    "Delhi", "Jammu and Kashmir", "Ladakh"
]

OCCUPATIONS = [
    "Student",
    "Unemployed",
    "Farmer / Agriculture",
    "Self-Employed / Business",
    "Private Sector Employee",
    "Government Employee",
    "Daily Wager / Artisan"
]

EDUCATION_LEVELS = [
    "Class 10 Pass",
    "Class 12 Pass",
    "Diploma / ITI",
    "Undergraduate (B.Tech / B.Sc / B.A / B.Com)",
    "Postgraduate (M.Tech / M.Sc / M.A / MBA)",
    "Doctorate / PhD"
]

UI_TEXT = {
    "English": {
        "home": "Home Dashboard",
        "profile": "Citizen Profile",
        "find_benefits": "Find Benefits For Me",
        "doc_readiness": "Document Readiness",
        "readiness_score": "Application Readiness",
        "deadlines": "Deadlines & Renewals",
        "document_reuse": "Document Reuse Engine",
        "ai_assistant": "AI Scheme Assistant",
        "why_qualify": "WHY YOU QUALIFY",
        "not_eligible": "NOT ELIGIBLE",
        "what_missing": "WHAT AM I MISSING?",
        "official_portal": "Apply on Official Portal",

        # Profile Page
        "profile_title": "Citizen Profile Management",
        "profile_desc": "Your demographic profile is used by the SchemeReady Rule Engine to evaluate benefit eligibility.",
        "reset_demo": "Reset to Demo Student",
        "full_name": "Full Name",
        "age": "Age (Years)",
        "gender": "Gender",
        "state": "State of Domicile",
        "district": "District",
        "category": "Social Category",
        "occupation": "Occupation",
        "is_student": "Currently Enrolled Student",
        "education": "Education Level",
        "income": "Annual Family Income (INR ₹)",
        "area": "Area Type",
        "save_profile": "💾 Save Profile & Re-evaluate Eligibility",

        # Scheme Page
        "schemes_title": "Find Benefits For Me",
        "schemes_desc": "Rule-based eligibility matching your profile against official government schemes.",
        "cat_filter": "Filter by Category",
        "status_filter": "Filter by Eligibility Status",
        "tab_eligible": "Qualified & Eligible",
        "tab_ineligible": "Not Eligible",
        "benefits_label": "Benefits",

        # Documents Page
        "docs_title": "Smart Document Readiness & Consistency Check",
        "docs_desc": "Manage document availability, upload sample proofs, extract structured data, and verify profile consistency.",
        "mark_avail": "Mark Available",
        "mark_miss": "Mark Missing",
        "upload_title": "Sample Document Upload & Automated OCR Verification",
        "upload_btn": "⚡ Process & Extract Document Data",

        # Readiness Page
        "readiness_title": "Application Readiness Engine",
        "readiness_desc": "Transparent, non-arbitrary mathematical readiness calculation.",
        "rule_eligibility": "1. Rule Eligibility",
        "doc_readiness_step": "2. Document Readiness",
        "missing_docs_hdr": "🚨 Missing Documents & Actionable Next Steps",

        # Deadlines Page
        "deadlines_title": "Deadlines, Renewals & Document Reuse Engine",
        "deadlines_desc": "Track application urgency, renewal requirements, and discover schemes compatible with your existing documents."
    },
    "Hindi": {
        "home": "मुख्य डैशबोर्ड",
        "profile": "नागरिक प्रोफाइल",
        "find_benefits": "मेरे लिए योजनाएं खोजें",
        "doc_readiness": "दस्तावेज़ तत्परता",
        "readiness_score": "आवेदन तत्परता स्कोर",
        "deadlines": "समय-सीमा और नवीनीकरण",
        "document_reuse": "दस्तावेज़ पुन: उपयोग इंजन",
        "ai_assistant": "एआई सहायक",
        "why_qualify": "आप क्यों पात्र हैं",
        "not_eligible": "अपात्र योजनाएं",
        "what_missing": "क्या कमी है?",
        "official_portal": "आधिकारिक पोर्टल पर आवेदन करें",

        # Profile Page
        "profile_title": "नागरिक प्रोफाइल प्रबंधन",
        "profile_desc": "आपकी जनसांख्यिकी प्रोफाइल का उपयोग योजना पात्रता के मूल्यांकन के लिए किया जाता है।",
        "reset_demo": "डेमो छात्र प्रोफाइल रीसेट करें",
        "full_name": "पूरा नाम",
        "age": "आयु (वर्ष)",
        "gender": "लिंग",
        "state": "मूल राज्य (Domicile)",
        "district": "ज़िला",
        "category": "सामाजिक वर्ग (Category)",
        "occupation": "व्यवसाय / पेशा",
        "is_student": "वर्तमान में अध्ययनरत छात्र",
        "education": "शिक्षा का स्तर",
        "income": "वार्षिक पारिवारिक आय (₹)",
        "area": "क्षेत्र का प्रकार (Urban/Rural)",
        "save_profile": "💾 प्रोफाइल सहेजें और पात्रता पुनः जांचें",

        # Scheme Page
        "schemes_title": "मेरे लिए योजनाएं खोजें",
        "schemes_desc": "आधिकारिक सरकारी योजनाओं के विरुद्ध आपकी प्रोफाइल का नियम-आधारित मिलान।",
        "cat_filter": "श्रेणी के अनुसार फ़िल्टर करें",
        "status_filter": "पात्रता स्थिति के अनुसार फ़िल्टर करें",
        "tab_eligible": "पात्र योजनाएं (Qualified & Eligible)",
        "tab_ineligible": "अपात्र योजनाएं (Not Eligible)",
        "benefits_label": "लाभ एवं सहायता",

        # Documents Page
        "docs_title": "स्मार्ट दस्तावेज़ तत्परता और निरंतरता जांच",
        "docs_desc": "दस्तावेज़ उपलब्धता प्रबंधित करें, नमूना प्रमाण अपलोड करें, और प्रोफाइल निरंतरता की जांच करें।",
        "mark_avail": "उपलब्ध चिह्नित करें",
        "mark_miss": "अनुपलब्ध चिह्नित करें",
        "upload_title": "नमूना दस्तावेज़ अपलोड और स्वचालित OCR सत्यापन",
        "upload_btn": "⚡ डेटा प्रोसेस एवं एक्सट्रैक्ट करें",

        # Readiness Page
        "readiness_title": "आवेदन तत्परता इंजन",
        "readiness_desc": "पारदर्शी, गणितीय तत्परता गणना।",
        "rule_eligibility": "1. नियम पात्रता",
        "doc_readiness_step": "2. दस्तावेज़ तत्परता",
        "missing_docs_hdr": "🚨 अनुपलब्ध दस्तावेज़ और आवश्यक कदम",

        # Deadlines Page
        "deadlines_title": "समय-सीमा, नवीनीकरण और दस्तावेज़ पुन: उपयोग",
        "deadlines_desc": "आवेदन की समय-सीमा, नवीनीकरण की आवश्यकताएं और पुन: उपयोग योग्य दस्तावेज़ देखें।"
    },
    "Hinglish": {
        "home": "Home Dashboard",
        "profile": "Citizen Profile",
        "find_benefits": "Find Benefits For Me",
        "doc_readiness": "Document Readiness",
        "readiness_score": "Application Readiness Score",
        "deadlines": "Deadlines & Renewals",
        "document_reuse": "Document Reuse Engine",
        "ai_assistant": "AI Assistant",
        "why_qualify": "Aap Kyun Qualify Karte Hain",
        "not_eligible": "Not Eligible Schemes",
        "what_missing": "What Am I Missing?",
        "official_portal": "Official Portal Par Apply Karein",

        # Profile Page
        "profile_title": "Citizen Profile Management",
        "profile_desc": "Aapki profile details ka use eligibility evaluate karne ke liye kiya jata hai.",
        "reset_demo": "Demo Student Profile Reset Karein",
        "full_name": "Full Name",
        "age": "Age (Years)",
        "gender": "Gender",
        "state": "State of Domicile",
        "district": "District",
        "category": "Social Category",
        "occupation": "Occupation",
        "is_student": "Currently Enrolled Student",
        "education": "Education Level",
        "income": "Annual Family Income (INR ₹)",
        "area": "Area Type",
        "save_profile": "💾 Profile Save Karein & Eligibility Check Karein",

        # Scheme Page
        "schemes_title": "Mere Liye Schemes Dhoondhein",
        "schemes_desc": "Rule-based eligibility matching your profile against official government schemes.",
        "cat_filter": "Category se Filter Karein",
        "status_filter": "Status se Filter Karein",
        "tab_eligible": "Qualified & Eligible Schemes",
        "tab_ineligible": "Not Eligible Schemes",
        "benefits_label": "Scheme Benefits",

        # Documents Page
        "docs_title": "Smart Document Readiness & Consistency Check",
        "docs_desc": "Documents upload karein, sample proofs verify karein aur status check karein.",
        "mark_avail": "Available Mark Karein",
        "mark_miss": "Missing Mark Karein",
        "upload_title": "Sample Document Upload & Automated OCR Verification",
        "upload_btn": "⚡ Document Process Karein",

        # Readiness Page
        "readiness_title": "Application Readiness Engine",
        "readiness_desc": "Transparent, non-arbitrary mathematical readiness calculation.",
        "rule_eligibility": "1. Rule Eligibility Status",
        "doc_readiness_step": "2. Document Readiness Status",
        "missing_docs_hdr": "🚨 Missing Documents & Next Action Steps",

        # Deadlines Page
        "deadlines_title": "Deadlines, Renewals & Document Reuse Engine",
        "deadlines_desc": "Track application deadlines, renewal schedules, and cross-scheme document reuse."
    }
}
