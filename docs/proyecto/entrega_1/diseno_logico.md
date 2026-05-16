---
proyecto: Gestión de Inventario
etapa: 1 - Diseño Lógico (Entrega 1)
materia: Lógica de Programación (LDP135)
estado: Completado
tags: [pseint, pseudocodigo, validaciones, arquitectura-limpia]
creado: 2026-05-15
---

# 📐 Diseño Lógico - Gestión de Inventario

Este documento contiene la especificación técnica de la lógica de negocio inicial del proyecto **Gestión de Inventario**. El diseño ha sido implementado y validado en pseudocódigo utilizando PSeInt, sirviendo como el plano arquitectónico antes de la traducción al código fuente definitivo en Python.

---

## 🧠 Estructura de Datos en Memoria

Debido a las limitaciones del entorno educativo de PSeInt para manejar estructuras complejas (como Clases u Objetos), el almacenamiento temporal se modeló utilizando el patrón de **Arreglos Paralelos**. 

Se definieron 4 vectores con una capacidad física máxima de 100 registros, vinculados lógicamente mediante un índice posicional común (`i`):

*   `lista_codigos[100]`: Identificador alfanumérico único del producto.
*   `lista_nombres[100]`: Descripción o nombre comercial.
*   `lista_cantidades[100]`: Stock físico disponible (entero).
*   `lista_precios[100]`: Costo unitario (real).


> [!IMPORTANT]
> 
> **Definición de Índices (Mañas del Entorno)**
> 
> El intérprete de PSeInt bajo la configuración institucional utiliza indexación **Base-1** (los arreglos van del 1 al 100). Para evitar desbordamientos de memoria (`Error 303`), el puntero global `v_total` se incrementa inmediatamente *antes* de realizar la persistencia de un nuevo registro. Al migrar a Python/FastAPI, esta lógica se transformará nativamente a **Base-0**.


---

## 🛡️ Reglas de Negocio y Validaciones

La arquitectura del código prioriza la integridad de los datos mediante tres capas de validación estricta en el módulo de registro:

### 1. Control de Duplicidad (Unicidad del Código)
Antes de aceptar un producto, el sistema realiza un barrido lineal del arreglo `lista_codigos`. Si el código ingresado coincide con uno existente, el registro se aborta inmediatamente.

> [!WARNING]
> 
> **Cláusula de Guarda para Inventario Vacío**
> 
> Ejecutar un ciclo de búsqueda `Para` desde 1 hasta `v_total` cuando el inventario no tiene elementos genera un quiebre de lógica en PSeInt. Para solucionar esto, la validación de unicidad está protegida por una condición de guarda (`Si v_total > 0 Entonces`), aislando el proceso en el primer registro.

### 2. Prevención de Stock Negativo
Para cumplir con las directrices de auditoría del inventario, la cantidad inicial no puede ser menor a cero. Se implementa un ciclo de reintento (`Mientras`) que bloquea al usuario hasta que provea un valor válido.

### 3. Integridad Financiera (Precios Mayores a Cero)
Al igual que el stock, el precio unitario se somete a un control de flujo cerrado para impedir valores negativos que alteren los cálculos financieros del backend.

---

## 🖥️ Flujo de Control de la Interfaz (CLI)

El menú interactivo se mantiene operativo mediante una evaluación continua de estados en un ciclo `Mientras`. 

```text
[Inicio] ──> ¿v_opcion es 0, 1 o 2?
                 │
                 ├── (Sí) ──> Desplegar Menú ──> Leer v_opcion
                 │               │
                 │               ├── [Opción 1] ──> RegistrarProducto() ──> v_opcion = 0
                 │               └── [Opción 2] ──> MostrarInventario() ──> v_opcion = 0
                 │
                 └── (No) ──> [Opción 3 / Salir] ──> FinAlgoritmo
```


> [!IMPORTANT]
> 
> **Optimización de Sintaxis para Perfiles Estrictos** 
>
>Para asegurar la compatibilidad total y evitar fallos de lectura, se reemplazó el comando `Segun` por condicionales `Si... Entonces` independientes y se sustituyó el operador `<>` por evaluaciones de igualdad lógica (`O`). Esto garantiza que el pseudocódigo corra sin importar qué tan estricto sea el compilador.


---

## 🚀 Próximo Paso: Del Pseudocódigo al Objeto Python

Este diseño lógico está desacoplado de la interfaz. En la **Fase 2**, los arreglos paralelos serán obsoletos:
1. Cada producto se modelará como un **Diccionario** o una instancia de clase (`models.py`).
2. El control de duplicados se resolverá eficientemente mediante consultas `SELECT` indexadas en SQLite (`repository.py`), eliminando la necesidad de bucles lineales manuales.