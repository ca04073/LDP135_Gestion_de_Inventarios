from cli import menus
from storage import database

def iniciar_aplicacion() -> None:
    database.inicializar_base_datos()
    while True:
        menus.limpiar_pantalla()
        opcion = menus.mostrar_menu_principal()
        if opcion == "1": menus.registrar_producto_ui()
        elif opcion == "2": menus.listar_inventario_ui()
        elif opcion == "3": menus.modificar_producto_ui()
        elif opcion == "4": menus.eliminar_producto_ui()
        elif opcion == "5": break
        input("\nPresione Enter para continuar...")
