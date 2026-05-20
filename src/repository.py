import json
from pathlib import Path
from typing import Dict, List

from src.models import Product, Order, OrderItem


class JsonRepository:
    def __init__(self, path: str) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._save({"products": [], "orders": []})

    def _load(self) -> dict:
        with self.path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self, payload: dict) -> None:
        with self.path.open("w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

    def list_products(self) -> List[Product]:
        data = self._load()
        return [Product(**p) for p in data["products"]]

    def add_product(self, product: Product) -> None:
        data = self._load()
        if any(p["sku"] == product.sku for p in data["products"]):
            raise ValueError("Ya existe un producto con ese SKU")
        data["products"].append(product.__dict__)
        self._save(data)

    def list_orders(self) -> List[Order]:
        data = self._load()
        orders: List[Order] = []
        for row in data["orders"]:
            items = [OrderItem(**item) for item in row["items"]]
            orders.append(
                Order(
                    id=row["id"],
                    customer=row["customer"],
                    created_at=row["created_at"],
                    items=items,
                )
            )
        return orders

    def add_order(self, order: Order) -> None:
        data = self._load()
        data["orders"].append(order.to_dict())
        self._save(data)

    def get_product_map(self) -> Dict[str, Product]:
        return {p.sku: p for p in self.list_products()}
