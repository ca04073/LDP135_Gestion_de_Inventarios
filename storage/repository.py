import sqlite3
from typing import List, Optional
from core.models import Producto
from storage.database import obtener_conexion 

def guardar_producto(producto: Producto) -> None:
    sql = "INSERT INTO productos (codigo, nombre, cantidad, precio, proveedor) VALUES (?, ?, ?, ?, ?);"
    try:
        with obtener_conexion() as conn:
            conn.execute(sql, (
                producto["codigo"], 
                producto["nombre"], 
                producto["cantidad"], 
                producto["precio"], 
                producto["proveedor"]
            ))
    except sqlite3.IntegrityError:
        raise ValueError(f"El código '{producto['codigo']}' ya existe.")

def buscar_por_codigo(codigo: str) -> Optional[Producto]:
    sql = "SELECT codigo, nombre, cantidad, precio, proveedor FROM productos WHERE codigo = ?;"
    with obtener_conexion() as conn:
        cursor = conn.execute(sql, (codigo,))
        fila = cursor.fetchone()
        return Producto(dict(fila)) if fila else None

def obtener_todos() -> List[Producto]:
    sql = "SELECT codigo, nombre, cantidad, precio, proveedor FROM productos;"
    with obtener_conexion() as conn:
        return [Producto(dict(fila)) for fila in conn.execute(sql).fetchall()]

def actualizar_producto(codigo: str, nombre: str, cantidad: int, precio: float, proveedor: str) -> None:
    sql = "UPDATE productos SET nombre = ?, cantidad = ?, precio = ?, proveedor = ? WHERE codigo = ?;"
    with obtener_conexion() as conn:
        cursor = conn.execute(sql, (nombre, cantidad, precio, proveedor, codigo))
        if cursor.rowcount == 0:
            raise ValueError(f"Producto '{codigo}' no encontrado.")

def borrar_producto(codigo: str) -> None:
    sql = "DELETE FROM productos WHERE codigo = ?;"
    with obtener_conexion() as conn:
        cursor = conn.execute(sql, (codigo,))
        if cursor.rowcount == 0:
            raise ValueError(f"Producto '{codigo}' no encontrado.")
