# Curso-gh-300

Aplicación en Python para gestionar productos y pedidos desde consola.

## Funcionalidades

- Alta de productos con SKU, nombre y precio.
- Listado de productos.
- Creación de pedidos con múltiples ítems.
- Listado de pedidos con detalle de líneas y total.
- Persistencia de datos en `data/store.json`.

## Estructura

- `app.py`: punto de entrada con menú interactivo.
- `src/models.py`: modelos de dominio (`Product`, `OrderItem`, `Order`).
- `src/repository.py`: repositorio JSON para lectura/escritura.
- `src/services.py`: lógica de negocio para productos y pedidos.

## Requisitos

- Python 3.10 o superior.

## Ejecución

Desde la raíz del proyecto:

```bash
python app.py
```

## Uso rápido

1. Crea uno o varios productos.
2. Crea pedidos usando el formato `SKU:cantidad,SKU:cantidad`.
3. Consulta el listado de pedidos y sus totales.
