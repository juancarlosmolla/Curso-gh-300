from src.repository import JsonRepository
from src.services import OrderService


def print_menu() -> None:
    print("\n=== Gestor de Pedidos ===")
    print("1. Crear producto")
    print("2. Listar productos")
    print("3. Crear pedido")
    print("4. Listar pedidos")
    print("5. Salir")


def create_product(service: OrderService) -> None:
    sku = input("SKU: ").strip()
    name = input("Nombre: ").strip()
    price = float(input("Precio: ").strip())
    product = service.create_product(sku, name, price)
    print(f"Producto creado: {product.sku} - {product.name} (${product.price:.2f})")


def list_products(service: OrderService) -> None:
    products = service.get_products()
    if not products:
        print("No hay productos registrados")
        return

    print("\nProductos:")
    for product in products:
        print(f"- {product.sku}: {product.name} (${product.price:.2f})")


def create_order(service: OrderService) -> None:
    customer = input("Cliente: ").strip()
    raw_items = input(
        "Items (formato SKU:cantidad,SKU:cantidad). Ejemplo: CAM-01:2,RAT-02:1\n> "
    ).strip()

    request_items = []
    for item in raw_items.split(","):
        sku, quantity = item.split(":")
        request_items.append((sku.strip(), int(quantity.strip())))

    order = service.create_order(customer, request_items)
    print(f"Pedido #{order.id} creado para {order.customer}")
    print(f"Total: ${order.total:.2f}")


def list_orders(service: OrderService) -> None:
    orders = service.get_orders()
    if not orders:
        print("No hay pedidos registrados")
        return

    print("\nPedidos:")
    for order in orders:
        print(f"- Pedido #{order.id} | Cliente: {order.customer} | Total: ${order.total:.2f}")
        for item in order.items:
            subtotal = item.quantity * item.unit_price
            print(
                f"  * {item.sku} x {item.quantity} @ ${item.unit_price:.2f} = ${subtotal:.2f}"
            )


def main() -> None:
    repository = JsonRepository("data/store.json")
    service = OrderService(repository)

    actions = {
        "1": create_product,
        "2": list_products,
        "3": create_order,
        "4": list_orders,
    }

    while True:
        try:
            print_menu()
            choice = input("Selecciona una opcion: ").strip()
            if choice == "5":
                print("Hasta luego")
                break
            action = actions.get(choice)
            if action is None:
                print("Opcion invalida")
                continue
            action(service)
        except ValueError as error:
            print(f"Error: {error}")
        except Exception as error:
            print(f"Error inesperado: {error}")


if __name__ == "__main__":
    main()
