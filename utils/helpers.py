from typing import Dict, Any, List
from sqlalchemy.orm import Session
from database.models import User, Scheme, UserDocument

def format_currency(amount: float) -> str:
    """Format float amount into Indian Rupee representation."""
    try:
        return f"₹{amount:,.0f}"
    except Exception:
        return f"₹{amount}"

def get_current_user_profile(db: Session) -> Dict[str, Any]:
    """Fetch current user profile from DB or default to Demo Student."""
    user = db.query(User).filter_by(is_demo=True).first()
    if not user:
        user = db.query(User).first()
    
    if user:
        return {
            "id": user.id,
            "name": user.name,
            "age": user.age,
            "gender": user.gender,
            "state": user.state,
            "district": user.district,
            "occupation": user.occupation,
            "is_student": user.is_student,
            "education_level": user.education_level,
            "annual_family_income": user.annual_family_income,
            "area_type": user.area_type,
            "category_type": user.category_type,
            "is_demo": user.is_demo
        }
    
    # Fallback default dictionary
    return {
        "id": 1,
        "name": "Demo Student",
        "age": 19,
        "gender": "General",
        "state": "Uttar Pradesh",
        "district": "Lucknow",
        "occupation": "Student",
        "is_student": True,
        "education_level": "B.Tech",
        "annual_family_income": 250000.0,
        "area_type": "Urban",
        "category_type": "General",
        "is_demo": True
    }

def get_user_documents(db: Session, user_id: int) -> List[Dict[str, Any]]:
    """Fetch all document records for user from DB."""
    docs = db.query(UserDocument).filter_by(user_id=user_id).all()
    results = []
    for d in docs:
        results.append({
            "id": d.id,
            "doc_id": d.doc_id,
            "doc_name": d.doc_name,
            "status": d.status,
            "file_path": d.file_path,
            "verification_notes": d.verification_notes
        })
    return results
