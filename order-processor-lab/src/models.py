"""Модели данных order-processor-lab."""

from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, field_validator

OrderId = Annotated[
    str,
    Field(pattern=r"^ORD-\d{6}$", description="Номер заказа, напр. ORD-000123"),
]
Money = Annotated[Decimal, Field(gt=0, max_digits=12, decimal_places=2)]


class RefundRequest(BaseModel):
    """Запрос на возврат товара по заказу."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    order_id: OrderId
    reason: str = Field(min_length=10, max_length=1000, description="Причина возврата")
    refund_amount: Money = Field(description="Сумма возврата, строго больше 0")

    @field_validator("reason")
    @classmethod
    def reason_must_not_be_blank(cls, value: str) -> str:
        if not any(char.isalpha() for char in value):
            raise ValueError("Причина возврата должна содержать текст, а не только символы")
        return value
