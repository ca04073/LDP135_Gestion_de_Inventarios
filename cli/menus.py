import os
from core import inventory

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu_principal() -> str:
    print("\n=== SISTEMA DE GESTION DE INVENTARIO ===")
    print("1. Registrar Producto\n2. Mostrar Inventario\n3. Modificar Producto\n4. Eliminar Producto\n5. Salir")
    return input("\nSeleccione una opcion: ")

def registrar_producto_ui() -> None:
    try:
        codigo = input("Codigo: ")
        nombre = input("Nombre: ")
        cantidad = int(input("Cantidad: "))
        precio = float(input("Precio: "))
        proveedor = input("Proveedor: ")
        inventory.registrar_nuevo_producto(codigo, nombre, cantidad, precio, proveedor)
        print("[!] Producto registrado.")
    except ValueError as e:
        print(f"[!] Error: {e}")

def listar_inventario_ui() -> None:
    productos = inventory.consultar_inventario()
    if not productos: 
        print("Inventario vacio.")
    else:
        print("=" * 73)
        print(f"{'CODIGO':^12} | {'NOMBRE':^15} | {'STOCK':^9} | {'PRECIO':^10} | {'PROVEEDOR':^15}")
        print("=" * 73)
        for p in productos:
            print(f"{p['codigo']:^12} | {p['nombre']:<15} | {p['cantidad']:>9} | ${p['precio']:>9.2f} | {p['proveedor']:<15}")
        print("=" * 73)

def modificar_producto_ui() -> None:
    codigo = input("Codigo a modificar: ")
    try:
        nombre = input("Nuevo nombre: ")
        cantidad = int(input("Nueva cantidad: "))
        precio = float(input("Nuevo precio: "))
        proveedor = input("Nuevo proveedor: ")
        inventory.modificar_producto(codigo, nombre, cantidad, precio, proveedor)
        print("[!] Producto actualizado por completo.")
    except ValueError as e:
        print(f"[!] Error: {e}")

def eliminar_producto_ui() -> None:
    codigo = input("Codigo a eliminar: ")
    try:
        inventory.eliminar_producto(codigo)
        print("[!] Producto eliminado.")
    except ValueError as e:
        print(f"[!] Error: {e}")
