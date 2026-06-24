import unittest
# Importamos la lógica del core. Ajusta el import según tu estructura exacta.
from core.inventory import inventory


class TestInventoryManager(unittest.TestCase):

    def setUp(self):
        """Este método se ejecuta ANTES de cada test.
        Ideal para inicializar un manager limpio en memoria."""
        self.manager = InventoryManager()

    def test_registrar_producto_exitoso(self):
        """Prueba que un producto válido se registre correctamente."""
        resultado = self.manager.registrar_producto(
            codigo="PROD001",
            nombre="Laptop Gamer",
            precio=1200.00,
            stock=10
        )
        self.assertTrue(resultado)

        # Validamos que el producto exista en la lista
        producto = self.manager.buscar_producto("PROD001")
        self.assertEqual(producto["nombre"], "Laptop Gamer")

    def test_registrar_precio_negativo_lanza_error(self):
        """Prueba que el core bloquee precios negativos lanzando ValueError."""
        # Verificamos que se dispare la excepción (Cláusula de guarda)
        with self.assertRaises(ValueError):
            self.manager.registrar_producto(
                codigo="PROD002",
                nombre="Mouse Óptico",
                precio=-15.00,  # 👈 Precio inválido
                stock=5
            )

    def test_registrar_stock_negativo_lanza_error(self):
        """Prueba que el core bloquee stock negativo lanzando ValueError."""
        with self.assertRaises(ValueError):
            self.manager.registrar_producto(
                codigo="PROD003",
                nombre="Teclado Mecánico",
                precio=45.00,
                stock=-2  # 👈 Stock inválido
            )


if __name__ == '__main__':
    unittest.main()
