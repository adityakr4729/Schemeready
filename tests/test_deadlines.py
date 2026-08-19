import pytest
from datetime import date, timedelta
from services.deadline_service import DeadlineService

def test_deadline_calculation_safe():
    future_date = (date.today() + timedelta(days=45)).strftime("%Y-%m-%d")
    status_info = DeadlineService.get_deadline_status(future_date)

    assert status_info["has_deadline"] is True
    assert status_info["days_remaining"] == 45
    assert status_info["status"] == "Safe"

def test_deadline_calculation_expired():
    past_date = (date.today() - timedelta(days=5)).strftime("%Y-%m-%d")
    status_info = DeadlineService.get_deadline_status(past_date)

    assert status_info["has_deadline"] is True
    assert status_info["days_remaining"] == -5
    assert status_info["status"] == "Expired"

def test_renewal_status():
    scheme_with_renewal = {"renewal_required": True, "renewal_information": "Annual renewal"}
    scheme_without_renewal = {"renewal_required": False}

    r1 = DeadlineService.get_renewal_status(scheme_with_renewal)
    r2 = DeadlineService.get_renewal_status(scheme_without_renewal)

    assert r1["renewal_required"] is True
    assert r1["status"] == "Upcoming"
    assert r2["renewal_required"] is False
    assert r2["status"] == "Not Required"
