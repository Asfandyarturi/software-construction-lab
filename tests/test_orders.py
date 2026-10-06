import pytest
from src.orders import calculate_order_total


def test_calculate_order_total() -> None:
    sample_order = {
        "items": [
            {"price": 25.0, "qty": 2},
            {"price": 40.0, "qty": 1},
            {"price": -5.0, "qty": 3},
        ],
        "member": True,
        "country": "PK",
    }

    result = calculate_order_total(sample_order)
    assert result == pytest.approx(86.0)