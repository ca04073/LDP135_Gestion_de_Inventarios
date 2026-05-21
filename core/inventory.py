from typing import List, Optional
from core.models import Producto
import storage.repository as repository

def registrar_nuevo_producto(codigo: str, nombre: str, cantidad: int, precio: float) -> None:
    if cantidad < 0 or precio < 0:
        raise ValueError("Valores negativos no permitidos.")
    nuevo: Producto = {"codigo": codigo, "nombre": nombre, "cantidad": cantidad, "precio": precio}
    repository.guardar_producto(nuevo)

def consultar_inventario() -> List[Producto]:
    return repository.obtener_todos()

def modificar_producto(codigo: str, nueva_cantidad: int, nuevo_precio: float) -> None:
    if nueva_cantidad < 0 or nuevo_precio < 0:
        raise ValueError("Valores negativos no permitidos.")
    repository.actualizar_producto(codigo, nueva_cantidad, nuevo_precio)

def eliminar_producto(codigo: str) -> None:
    repository.borrar_producto(codigo)