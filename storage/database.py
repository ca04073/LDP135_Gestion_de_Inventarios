import sqlite3

DB_NAME = "storage/inventario.db"

def obtener_conexion() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def inicializar_base_datos() -> None:
    sql_tabla = """
    CREATE TABLE IF NOT EXISTS productos (
        codigo TEXT PRIMARY KEY,
        nombre TEXT NOT NULL,
        cantidad INTEGER NOT NULL CHECK(cantidad >= 0),
        precio REAL NOT NULL CHECK(precio >= 0.0),
        proveedor TEXT NOT NULL DEFAULT 'No asignado'
    );
    """
    with obtener_conexion() as conn:
        conn.execute(sql_tabla)
