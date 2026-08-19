from datetime import datetime, date
from typing import Dict, Any, Optional

class DeadlineService:
    @staticmethod
    def get_deadline_status(deadline_str: Optional[str]) -> Dict[str, Any]:
        """
        Calculate remaining days and urgency status dynamically using Python datetime.
        """
        if not deadline_str:
            return {
                "has_deadline": False,
                "deadline_date": None,
                "days_remaining": None,
                "status": "Unknown",
                "label": "Deadline information not available",
                "color": "gray"
            }

        try:
            target_date = datetime.strptime(deadline_str, "%Y-%m-%d").date()
            today = date.today()
            days_remaining = (target_date - today).days

            if days_remaining < 0:
                status = "Expired"
                color = "#dc3545" # Red
                label = f"Expired ({abs(days_remaining)} days ago)"
            elif days_remaining <= 10:
                status = "Urgent"
                color = "#d9534f" # Bright red/orange
                label = f"Urgent ({days_remaining} days remaining)"
            elif days_remaining <= 30:
                status = "Approaching"
                color = "#f0ad4e" # Yellow/Orange
                label = f"Approaching ({days_remaining} days remaining)"
            else:
                status = "Safe"
                color = "#28a745" # Green
                label = f"Safe ({days_remaining} days remaining)"

            return {
                "has_deadline": True,
                "deadline_date": target_date.strftime("%d %B %Y"),
                "days_remaining": days_remaining,
                "status": status,
                "label": label,
                "color": color
            }
        except ValueError:
            return {
                "has_deadline": False,
                "deadline_date": None,
                "days_remaining": None,
                "status": "Unknown",
                "label": "Invalid deadline format",
                "color": "gray"
            }

    @staticmethod
    def get_renewal_status(scheme_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract renewal requirement and status.
        """
        renewal_required = scheme_dict.get("renewal_required", False)
        renewal_info = scheme_dict.get("renewal_information", "")

        if renewal_required:
            return {
                "renewal_required": True,
                "status": "Upcoming",
                "information": renewal_info if renewal_info else "Annual renewal required.",
                "color": "#17a2b8"
            }
        else:
            return {
                "renewal_required": False,
                "status": "Not Required",
                "information": "Renewal not required / information unavailable.",
                "color": "#6c757d"
            }
