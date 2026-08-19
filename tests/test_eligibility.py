import pytest
from services.eligibility_engine import RuleEngine

def test_eligible_user():
    user_profile = {
        "age": 19,
        "state": "Uttar Pradesh",
        "is_student": True,
        "annual_family_income": 250000.0,
        "gender": "General"
    }

    scheme_dict = {
        "scheme_id": "SCH001",
        "scheme_name": "UP Post-Matric Scholarship",
        "eligibility_rules": [
            {"field": "state", "operator": "eq", "value": "Uttar Pradesh", "label": "UP Domicile", "failure_reason": "Not UP Domicile"},
            {"field": "is_student", "operator": "eq", "value": True, "label": "Student Status", "failure_reason": "Not a student"},
            {"field": "annual_family_income", "operator": "lte", "value": 250000.0, "label": "Income <= 2.5L", "failure_reason": "Income exceeds limit"},
            {"field": "age", "operator": "gte", "value": 16, "label": "Age >= 16", "failure_reason": "Underage"},
            {"field": "age", "operator": "lte", "value": 30, "label": "Age <= 30", "failure_reason": "Overage"}
        ]
    }

    result = RuleEngine.evaluate_scheme(user_profile, scheme_dict)
    assert result.is_eligible is True
    assert result.passed_count == 5
    assert result.total_count == 5

def test_ineligible_user_high_income():
    user_profile = {
        "age": 19,
        "state": "Uttar Pradesh",
        "is_student": True,
        "annual_family_income": 500000.0,  # Exceeds 250k limit
        "gender": "General"
    }

    scheme_dict = {
        "scheme_id": "SCH001",
        "scheme_name": "UP Post-Matric Scholarship",
        "eligibility_rules": [
            {"field": "state", "operator": "eq", "value": "Uttar Pradesh", "label": "UP Domicile", "failure_reason": "Not UP Domicile"},
            {"field": "annual_family_income", "operator": "lte", "value": 250000.0, "label": "Income <= 2.5L", "failure_reason": "Income exceeds limit"}
        ]
    }

    result = RuleEngine.evaluate_scheme(user_profile, scheme_dict)
    assert result.is_eligible is False
    assert result.passed_count == 1
    assert any("Income exceeds limit" in r.failure_reason for r in result.evaluations if not r.passed)
