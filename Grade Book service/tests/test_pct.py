import gradebook


def test_student_with_no_marks_returns_zero(loaded: dict) -> None:
    assert gradebook.pct("S1") == "0"


def test_single_mark_calculates_correct_percentage(loaded: dict) -> None:
    loaded["marks"].append({"student": "S1", "assessment": "A1", "score": 15})
    assert gradebook.pct("S1") == "7.5"


def test_mark_for_unknown_assessment_is_ignored(loaded: dict) -> None:
    loaded["marks"].append({"student": "S1", "assessment": "GHOST", "score": 5})
    assert gradebook.pct("S1") == "0"
