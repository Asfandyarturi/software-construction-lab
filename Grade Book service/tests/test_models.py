import pytest
import models 


@pytest.mark.parametrize(
    "input_val",
    [
        pytest.param("15", id="str-int"),
        pytest.param(15, id="raw-int"),
        pytest.param("2.5", id="str-float"),
    ],
)
def test_parse_number_valid(input_val: object) -> None:
    assert models.parse_number(input_val) is not None


@pytest.mark.parametrize(
    "input_val",
    [
        pytest.param("abc", id="string"),
        pytest.param(True, id="bool"),
        pytest.param(None, id="none"),
        pytest.param([], id="list"),
        pytest.param("nan", id="nan"),
        pytest.param("inf", id="inf"),
    ],
)
def test_parse_number_invalid(input_val: object) -> None:
    with pytest.raises((ValueError, TypeError)):
        models.parse_number(input_val)
