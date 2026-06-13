---
proyecto: Gestión de Inventario
etapa: 2 - Arquitectura del Backend (Entrega 2)
materia: Lógica de Programación (LDP135)
estado: En Desarrollo
tags: [python, sqlite, arquitectura-hibrida, typeddict, doc-as-code]
creado: 2026-05-20
---

# 🧠 Arquitectura del Backend e Infraestructura de Datos

Este documento especifica las decisiones de diseño tomadas para la Fase 2 del proyecto **Gestión de Inventario**. Detalla la justificación técnica de la arquitectura híbrida implementada en la capa de datos y el mapeo de memoria hacia el motor incrustado SQLite.

---

## ⚖️ Justificación de la Arquitectura Híbrida

Para la gestión de los productos, se evaluaron dos enfoques tradicionales en Python: el uso de Clases con Programación Orientada a Objetos (POO) y el uso de Diccionarios puros. Finalmente, se optó por un **enfoque mixto/híbrido** que extrae las ventajas de ambos mundos:

### 1. Ligereza en Tiempo de Ejecución (`TypedDict`)
En lugar de instanciar clases pesadas que generan sobrecarga en la memoria para un sistema CLI/API, los productos se manejan en el entorno de Python como diccionarios nativos. Utilizando `typing.TypedDict` en `core/models.py`, el sistema cuenta con un tipado fuerte en tiempo de desarrollo (auto-completado, detección de errores en el editor), pero mantiene la velocidad de ejecución y la ligereza de un diccionario estándar.

### 2. Abstracción Estilo ORM (`sqlite3.Row`)
A través de la propiedad nativa `row_factory = sqlite3.Row` en la capa de persistencia (`storage/database.py`), el sistema transforma las tuplas planas devueltas por SQLite en objetos accesibles por llave. Esto permite al desarrollador interactuar con cada fila de la base de datos de manera semántica (`producto["nombre"]`), simulando la experiencia de un Object-Relational Mapper (ORM) sin la penalización de rendimiento ni la complejidad de dependencias externas como SQLAlchemy.

> [!IMPORTANT]
> 
> **Principio de Aislamiento Arquitectónico**
> 
> La capa de presentación (`cli/`) y el núcleo del negocio (`core/`) son completamente agnósticos de la base de datos. Consumen y procesan estructuras `Producto` (Diccionarios tipados). Si en el futuro se decide migrar el motor a PostgreSQL o BonsaiDB, el código del core permanecerá intacto; solo se modificará el adaptador de persistencia en `storage/`.

---

## 🛠️ Protocolo de Evolución del Modelo (Control de Cambios)

Dado que SQLite maneja un esquema rígido en disco, cualquier modificación en la estructura del modelo (por ejemplo, añadir campos como `proveedor` o `categoría`) requiere una actualización síncrona en tres niveles del repositorio:

```text
[Modificación en core/models.py]
               │
               ▼
[Actualización de Query en storage/database.py]
               │
               ▼
[Re-creación / Migración de la base de datos física]

```

>[!WARNING] 
>
>**Persistencia en Entornos de Desarrollo** 
>
>Modificar el archivo `models.py` no altera la base de datos física `inventario.db` si esta ya ha sido creada. Durante la fase académica de desarrollo, tras alterar el esquema, se debe eliminar físicamente el archivo `.db` local para forzar al módulo `database.py` a ejecutar el bloque `CREATE TABLE` con la nueva estructura en el siguiente arranque.

## 🖥️ Capa de Presentación (CLI)

La interfaz de usuario se implementó bajo un patrón de **Desacoplamiento Estricto**. El módulo `cli/menus.py` funciona únicamente como un canal de I/O (Input/Output).

> [!IMPORTANT]
> 
> **Gestión de Excepciones de Negocio**
> 
> La CLI actúa como el punto de captura de errores (`try-except`). No contiene lógica de validación; simplemente recibe las excepciones `ValueError` lanzadas por el Core y las traduce a mensajes de retroalimentación amigables para el usuario final. Esto asegura que el sistema sea robusto ante entradas inesperadas sin comprometer la integridad del Core.

> [!TIP]
> 
> **Formateo de Salida**
> 
> Se utiliza el formateo avanzado de `f-strings` para alinear las columnas del inventario, garantizando una visualización profesional en terminales estándar de consola (Windows/Linux).

## ⚙️ Expansión de Operaciones CRUD
El sistema se ha escalado para soportar el ciclo de vida completo de los datos:
* **Modificación (Update):** Implementada mediante `UPDATE` con validación de existencia vía `rowcount`.
* **Eliminación (Delete):** Implementada mediante `DELETE` con manejo de excepciones para códigos inexistentes.
* **UX/UI:** Se integró una utilidad de limpieza de consola (`os.system`) para mejorar la legibilidad y presentación del sistema en terminales interactivas.

## ⚙️ Expansión del Modelo de Datos y Operaciones CRUD (Fase 2.5)

Para cumplir con los nuevos requerimientos operativos, el ecosistema evolucionó hacia un sistema de persistencia total y gestión extendida.

### 1. Evolución del Esquema de Datos
Se incorporó el atributo `proveedor` en todas las capas del sistema bajo un principio de tipado estricto:
* **Capa Física (SQLite):** Columna `proveedor TEXT NOT NULL DEFAULT 'No Asignado'`.
* **Capa Lógica (Python):** Extensión del tipo estructurado `Producto` (`TypedDict`).

### 2. Ampliación del Núcleo (Core) y Persistencia
Se rompió la naturaleza de solo lectura/registro de la entrega anterior mediante la implementación de dos nuevas capacidades arquitectónicas en `storage/repository.py` y `core/inventory.py`:
* **Modificación Integral (Update):** Permite la mutación controlada de todos los campos de un artículo existente (Nombre, Stock, Precio, Proveedor) mediante consultas SQL parametrizadas, validando previamente que los valores numéricos cumplan con las cláusulas de guarda (no negativos).
* **Eliminación Definitiva (Delete):** Remueve registros de la base de datos basándose en su clave primaria (`codigo`), manejando excepciones semánticas (`ValueError`) mediante la verificación de filas afectadas (`cursor.rowcount == 0`) si el identificador no existe.
