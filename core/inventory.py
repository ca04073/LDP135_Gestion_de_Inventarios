from typing import List, Optional
from core.models import Producto
from storage import repository

def registrar_nuevo_producto(codigo: str, nombre: str, cantidad: int, precio: float, proveedor: str) -> None:
    if cantidad < 0 or precio < 0:
        raise ValueError("Valores negativos no permitidos.")
    if not nombre.strip() or not proveedor.strip():
        raise ValueError("El nombre y el proveedor no pueden estar vacíos.")
        
    nuevo: Producto = {
        "codigo": codigo, 
        "nombre": nombre, 
        "cantidad": cantidad, 
        "precio": precio, 
        "proveedor": proveedor
    }
    repository.guardar_producto(nuevo)

def consultar_inventario() -> List[Producto]:
    return repository.obtener_todos()

def modificar_producto(codigo: str, nuevo_nombre: str, nueva_cantidad: int, nuevo_precio: float, nuevo_proveedor: str) -> None:
    if nueva_cantidad < 0 or nuevo_precio < 0:
        raise ValueError("Valores negativos no permitidos.")
    if not nuevo_nombre.strip() or not nuevo_proveedor.strip():
        raise ValueError("El nombre y el proveedor no pueden estar vacíos.")
        
    repository.actualizar_producto(codigo, nuevo_nombre, nueva_cantidad, nuevo_precio, nuevo_proveedor)

def eliminar_producto(codigo: str) -> None:
    repository.borrar_producto(codigo)
