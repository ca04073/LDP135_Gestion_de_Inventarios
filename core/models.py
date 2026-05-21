from typing import TypedDict

class Producto(TypedDict):
    codigo: str
    nombre: str
    cantidad: int
    precio: float