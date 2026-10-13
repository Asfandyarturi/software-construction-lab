import pytest
import gradebook


@pytest.fixture
def state() -> dict:
    return {
        "students": {"S1": {"id": "S1", "name": "Asfandyar"}},
        "assessments": {
            "A1": {"id": "A1", "weight": 10.0, "total": 20.0},
            "A2": {"id": "A2", "weight": 30.0, "total": 50.0},
        },
        "marks": [],
    }


@pytest.fixture
def loaded(state: dict, monkeypatch: pytest.MonkeyPatch) -> dict:
    monkeypatch.setattr(gradebook, "STATE", state)
    return state
