from typing import Dict, Any, List
from dataclasses import dataclass, field

@dataclass
class RuleEvaluation:
    field: str
    label: str
    current_value: Any
    required_value: Any
    operator: str
    passed: bool
    failure_reason: str

@dataclass
class EligibilityResult:
    scheme_id: str
    scheme_name: str
    is_eligible: bool
    evaluations: List[RuleEvaluation] = field(default_factory=list)
    passed_count: int = 0
    total_count: int = 0
    explanation: str = ""

class RuleEngine:
    @staticmethod
    def evaluate_rule(field_name: str, operator: str, target_val: Any, user_val: Any) -> bool:
        """Evaluate a single rule deterministically."""
        if user_val is None:
            return False
        
        # String normalization for comparison
        if isinstance(user_val, str) and isinstance(target_val, str):
            user_val_str = user_val.strip().lower()
            target_val_str = target_val.strip().lower()
            if operator == "eq":
                return user_val_str == target_val_str
            elif operator == "neq":
                return user_val_str != target_val_str
            elif operator == "in":
                return user_val_str in target_val_str
        
        if operator == "eq":
            return user_val == target_val
        elif operator == "neq":
            return user_val != target_val
        elif operator == "gte":
            return user_val >= target_val
        elif operator == "lte":
            return user_val <= target_val
        elif operator == "gt":
            return user_val > target_val
        elif operator == "lt":
            return user_val < target_val
        elif operator == "in":
            if isinstance(target_val, list):
                # case-insensitive check if list of strings
                if user_val and isinstance(user_val, str):
                    return any(user_val.strip().lower() == str(item).strip().lower() for item in target_val)
                return user_val in target_val
            return False
        return False

    @classmethod
    def evaluate_scheme(cls, user_profile: Dict[str, Any], scheme_dict: Dict[str, Any]) -> EligibilityResult:
        """
        Evaluate user_profile against all eligibility_rules of a scheme.
        """
        scheme_id = scheme_dict.get("scheme_id", "")
        scheme_name = scheme_dict.get("scheme_name", "")
        rules = scheme_dict.get("eligibility_rules", [])

        evaluations: List[RuleEvaluation] = []
        all_passed = True

        for rule in rules:
            field_name = rule.get("field")
            operator = rule.get("operator")
            target_value = rule.get("value")
            label = rule.get("label", f"Check {field_name}")
            failure_reason = rule.get("failure_reason", f"Failed requirement for {field_name}")

            user_value = user_profile.get(field_name)
            
            passed = cls.evaluate_rule(field_name, operator, target_value, user_value)
            if not passed:
                all_passed = False

            evaluations.append(
                RuleEvaluation(
                    field=field_name,
                    label=label,
                    current_value=user_value,
                    required_value=target_value,
                    operator=operator,
                    passed=passed,
                    failure_reason=failure_reason
                )
            )

        passed_count = sum(1 for e in evaluations if e.passed)
        total_count = len(evaluations)

        if all_passed:
            explanation = "You satisfy all required eligibility criteria for this scheme."
        else:
            failed_reasons = [e.failure_reason for e in evaluations if not e.passed]
            explanation = f"Not eligible due to: {'; '.join(failed_reasons)}"

        return EligibilityResult(
            scheme_id=scheme_id,
            scheme_name=scheme_name,
            is_eligible=all_passed,
            evaluations=evaluations,
            passed_count=passed_count,
            total_count=total_count,
            explanation=explanation
        )
