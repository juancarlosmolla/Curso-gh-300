from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List


@dataclass
class Product:
    sku: str
    name: str
    price: float


@dataclass
class OrderItem:
    sku: str
    quantity: int
    unit_price: float


@dataclass
class Order:
    id: int
    customer: str
    created_at: str
    items: List[OrderItem]

    @property
    def total(self) -> float:
        return sum(item.quantity * item.unit_price for item in self.items)

    @staticmethod
    def new(order_id: int, customer: str, items: List[OrderItem]) -> "Order":
        return Order(
            id=order_id,
            customer=customer,
            created_at=datetime.now().isoformat(timespec="seconds"),
            items=items,
        )

    def to_dict(self) -> dict:
        payload = asdict(self)
        payload["total"] = round(self.total, 2)
        return payload
