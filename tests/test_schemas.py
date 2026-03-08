import pytest

from src.core.schemas import WorkflowBlueprint


def test_blueprint_validation():
    """Verifies that the system correctly validates a Workflow Blueprint."""
    sample_data = {
        "workflow_id": "TEST-001",
        "employee_id": "EMP-TEST",
        "intent_summary": "Test Intent",
        "persistence": {
            "daily_counts": {"2026-02-23": 1},
            "is_2day_persistent": False,
            "is_3day_persistent": False,
            "is_4day_persistent": False,
            "total_occurrences": 1
        },
        "steps": []
    }
    # This should pass without error
    blueprint = WorkflowBlueprint(**sample_data)
    assert blueprint.workflow_id == "TEST-001"

def test_invalid_action_type():
    """Verifies that the system rejects invalid ActionTypes."""
    from pydantic import ValidationError
    with pytest.raises(ValidationError):
        # 'FLY_A_PLANE' is not a valid ActionType enum
        WorkflowBlueprint(workflow_id="X", employee_id="Y", intent_summary="Z", 
                          persistence={}, steps=[{"action": "FLY_A_PLANE"}])