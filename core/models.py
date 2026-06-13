from typing import TypedDict

class Producto(TypedDict):
    codigo: str
    nombre: str
    cantidad: int
    precio: float
    proveedor: str      #   Nueva columna incorporada
