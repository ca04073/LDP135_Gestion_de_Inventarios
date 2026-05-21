import os
from core import inventory

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu_principal() -> str:
    print("\n=== SISTEMA DE GESTION DE INVENTARIO ===")
    print("\n1. Registrar Producto\n2. Mostrar Inventario\n3. Modificar Producto\n4. Eliminar Producto\n5. Salir")
    return input("\nSeleccione una opcion: ")

def registrar_producto_ui() -> None:
    try:
        codigo = input("Codigo: ")
        nombre = input("Nombre: ")
        cantidad = int(input("Cantidad: "))
        precio = float(input("Precio: "))
        inventory.registrar_nuevo_producto(codigo, nombre, cantidad, precio)
        print("\n[!] Producto registrado.")
    except ValueError as e:
        print(f"\n[!] Error: {e}")

def listar_inventario_ui() -> None:
    productos = inventory.consultar_inventario()
    if not productos: print("\nInventario vacio.")
    else:
        print(f"\n{'CODIGO':<10} | {'NOMBRE':<15} | {'STOCK':<8} | {'PRECIO':<8}")
        for p in productos:
            print(f"{p['codigo']:<10} | {p['nombre']:<15} | {p['cantidad']:<8} | ${p['precio']:<8.2f}")

def modificar_producto_ui() -> None:
    codigo = input("\nCodigo a modificar: ")
    try:
        cantidad = int(input("Nueva cantidad: "))
        precio = float(input("Nuevo precio: "))
        inventory.modificar_producto(codigo, cantidad, precio)
        print("\n[!] Producto actualizado.")
    except ValueError as e:
        print(f"\n[!] Error: {e}")

def eliminar_producto_ui() -> None:
    codigo = input("\nCodigo a eliminar: ")
    try:
        inventory.eliminar_producto(codigo)
        print("\n[!] Producto eliminado.")
    except ValueError as e:
        print(f"\n[!] Error: {e}")