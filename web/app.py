from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# Importamos la lógica de negocio
from storage import database
from core import inventory

app = FastAPI(title="Gestión de Inventario Web")

templates = Jinja2Templates(directory="web/templates")

# Montamos la carpeta física
app.mount("/static", StaticFiles(directory="web/static"), name="static")

@app.on_event("startup")
def startup_event():
    database.inicializar_base_datos()

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    """Renderiza la página completa al cargar por primera vez."""
    productos = inventory.consultar_inventario()
    contexto = {"request": request, "productos": productos}
    return templates.get_template("index.html").render(contexto)

@app.get("/productos/tabla", response_class=HTMLResponse)
def obtener_tabla_html(request: Request):
    """Ruta interna: Devuelve SOLO las filas de la tabla en HTML puro."""
    productos = inventory.consultar_inventario()
    contexto = {"request": request, "productos": productos}
    return templates.get_template("componentes/filas_tabla.html").render(contexto)

@app.post("/productos", response_class=HTMLResponse)
def registrar_producto_web(
        request: Request,
        codigo: str = Form(...),
        nombre: str = Form(...),
        cantidad: int = Form(...),
        precio: float = Form(...),
        proveedor: str = Form(...)
):
    """Recibe los datos del formulario web, registra y pide actualizar la tabla."""
    try:
        # Ejecutamos exactamente la misma lógica del CLI
        inventory.registrar_nuevo_producto(codigo, nombre, cantidad, precio, proveedor)
    except ValueError as e:
        # Mandamos un encabezado de respuesta HTTP para que HTMX pueda capturar el error si quisiéramos
        pass

    # Redirigimos internamente a la ruta que redibuja las filas
    return obtener_tabla_html(request)

@app.delete("/productos/{codigo}", response_class=HTMLResponse)
def eliminar_producto_web(codigo: str):
    """Elimina el producto por su código y responde un string vacío para que HTMX remueva la fila."""
    try:
        inventory.eliminar_producto(codigo)
    except ValueError:
        pass
    # Al responder un string vacío con hx-swap="outerHTML", HTMX borra la fila de la pantalla
    return ""

@app.post("/productos/actualizar", response_class=HTMLResponse)
def actualizar_producto_web(
    request: Request,
    codigo: str = Form(...),
    nombre: str = Form(...),
    cantidad: int = Form(...),
    precio: float = Form(...),
    proveedor: str = Form(...)
):
    """Procesa la actualización completa de un artículo y refresca la tabla."""
    try:
        inventory.modificar_producto(codigo, nombre, cantidad, precio, proveedor)
    except ValueError:
        pass
    return obtener_tabla_html(request)