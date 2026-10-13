import pytest
import gradebook


@pytest.mark.parametrize(
    ("marks", "expected"),
    [
        pytest.param([], "0", id="no-marks"),
        pytest.param([("A1", 15)], "7.5", id="A1=15->7.5"),
        pytest.param([("A1", 20)], "10.0", id="A1=20->10.0"),
        pytest.param([("A1", 0)], "0.0", id="A1=0->0.0"),
        pytest.param([("A1", 15), ("A2", 40)], "31.5", id="A1=15-and-A2=40->31.5"),
    ],
)
def test_pct_calculations(loaded: dict, marks: list[tuple[str, float]], expected: str) -> None:
    for assessment, score in marks:
        loaded["marks"].append({"student": "S1", "assessment": assessment, "score": score})
    assert gradebook.pct("S1") == expected


def test_mark_for_unknown_assessment_is_ignored(loaded: dict) -> None:
    loaded["marks"].append({"student": "S1", "assessment": "GHOST", "score": 5})
    assert gradebook.pct("S1") == "0"
