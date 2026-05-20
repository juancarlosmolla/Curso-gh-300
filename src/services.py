from typing import List, Tuple

from src.models import Product, Order, OrderItem
from src.repository import JsonRepository


class OrderService:
    def __init__(self, repository: JsonRepository) -> None:
        self.repository = repository

    def create_product(self, sku: str, name: str, price: float) -> Product:
        if price <= 0:
            raise ValueError("El precio debe ser mayor que cero")
        product = Product(sku=sku.strip(), name=name.strip(), price=round(price, 2))
        self.repository.add_product(product)
        return product

    def get_products(self) -> List[Product]:
        return self.repository.list_products()

    def create_order(self, customer: str, request_items: List[Tuple[str, int]]) -> Order:
        if not customer.strip():
            raise ValueError("El cliente es obligatorio")

        product_map = self.repository.get_product_map()
        if not product_map:
            raise ValueError("No hay productos cargados")

        items: List[OrderItem] = []
        for sku, quantity in request_items:
            if sku not in product_map:
                raise ValueError(f"El SKU '{sku}' no existe")
            if quantity <= 0:
                raise ValueError("La cantidad debe ser mayor que cero")
            product = product_map[sku]
            items.append(
                OrderItem(sku=product.sku, quantity=quantity, unit_price=product.price)
            )

        orders = self.repository.list_orders()
        next_id = max((order.id for order in orders), default=0) + 1
        order = Order.new(next_id, customer.strip(), items)
        self.repository.add_order(order)
        return order

    def get_orders(self) -> List[Order]:
        return self.repository.list_orders()
