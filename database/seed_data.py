import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if sys.path and sys.path[0] == current_dir:
    sys.path.pop(0)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import json
from sqlalchemy.orm import Session
from database.database import init_db, SessionLocal
from database.models import User, Scheme, EligibilityRule, RequiredDocument, UserDocument

def seed_database(force: bool = False):
    """Seed SQLite database with initial schemes and demo student profile."""
    init_db()
    db: Session = SessionLocal()
    try:
        scheme_count = db.query(Scheme).count()
        if scheme_count == 0 or force:
            if force:
                db.query(UserDocument).delete()
                db.query(RequiredDocument).delete()
                db.query(EligibilityRule).delete()
                db.query(Scheme).delete()
                db.commit()

            json_path = os.path.join(parent_dir, "data", "schemes.json")
            if os.path.exists(json_path):
                with open(json_path, "r", encoding="utf-8") as f:
                    schemes_data = json.load(f)
                
                for s_data in schemes_data:
                    rules_data = s_data.pop("eligibility_rules", [])
                    docs_data = s_data.pop("required_documents", [])
                    
                    scheme = Scheme(**s_data)
                    db.add(scheme)
                    db.flush()

                    for r in rules_data:
                        rule = EligibilityRule(scheme_id=scheme.scheme_id, **r)
                        db.add(rule)
                    
                    for d in docs_data:
                        doc = RequiredDocument(scheme_id=scheme.scheme_id, **d)
                        db.add(doc)

                db.commit()
                print(f"[Seed] Successfully seeded {len(schemes_data)} schemes.")

        # Seed Demo Student Profile
        demo_user = db.query(User).filter_by(is_demo=True).first()
        if not demo_user:
            demo_user = User(
                name="Demo Student",
                age=19,
                gender="General",
                state="Uttar Pradesh",
                district="Lucknow",
                occupation="Student",
                is_student=True,
                education_level="B.Tech",
                annual_family_income=250000.0,
                area_type="Urban",
                category_type="General",
                is_demo=True
            )
            db.add(demo_user)
            db.commit()
            db.refresh(demo_user)
            print("[Seed] Successfully seeded Demo Student profile.")

        # Seed initial documents for Demo Student (4/5 documents ready for scenario)
        user_docs_count = db.query(UserDocument).filter_by(user_id=demo_user.id).count()
        if user_docs_count == 0 or force:
            if force:
                db.query(UserDocument).filter_by(user_id=demo_user.id).delete()
                db.commit()

            initial_docs = [
                {"doc_id": "DOC_AADHAAR", "doc_name": "Aadhaar Card", "status": "Available", "verification_notes": "Aadhaar verified"},
                {"doc_id": "DOC_DOMICILE", "doc_name": "Domicile Certificate", "status": "Available", "verification_notes": "UP Domicile verified"},
                {"doc_id": "DOC_MARKSHEET", "doc_name": "Educational Marksheet", "status": "Available", "verification_notes": "12th Marksheet verified"},
                {"doc_id": "DOC_BANK", "doc_name": "Bank Passbook", "status": "Available", "verification_notes": "DBT active"},
            ]
            for doc in initial_docs:
                user_doc = UserDocument(
                    user_id=demo_user.id,
                    doc_id=doc["doc_id"],
                    doc_name=doc["doc_name"],
                    status=doc["status"],
                    verification_notes=doc["verification_notes"]
                )
                db.add(user_doc)
            db.commit()
            print("[Seed] Seeded initial demo documents (4/5 ready).")

    except Exception as e:
        db.rollback()
        print(f"[Seed Error] Failed to seed database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database(force=True)
