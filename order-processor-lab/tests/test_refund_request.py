from decimal import Decimal

import pytest
from pydantic import ValidationError

from src.models import RefundRequest


def test_valid_refund_request() -> None:
    refund = RefundRequest(
        order_id="ORD-000123",
        reason="  Товар пришёл повреждённым  ",
        refund_amount="1500.50",
    )

    assert refund.order_id == "ORD-000123"
    assert refund.reason == "Товар пришёл повреждённым"
    assert refund.refund_amount == Decimal("1500.50")


def test_short_reason_is_rejected() -> None:
    with pytest.raises(ValidationError) as error:
        RefundRequest(order_id="ORD-000123", reason="Брак", refund_amount=100)

    assert error.value.errors()[0]["loc"] == ("reason",)
    assert error.value.errors()[0]["type"] == "string_too_short"


@pytest.mark.parametrize("amount", [0, -1, "-0.01"])
def test_non_positive_amount_is_rejected(amount: int | str) -> None:
    with pytest.raises(ValidationError) as error:
        RefundRequest(order_id="ORD-000123", reason="Не подошёл размер", refund_amount=amount)

    assert error.value.errors()[0]["loc"] == ("refund_amount",)
    assert error.value.errors()[0]["type"] == "greater_than"
