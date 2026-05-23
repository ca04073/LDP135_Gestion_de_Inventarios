---
proyecto: Gestión de Inventario
estado: En Desarrollo
materia: Lógica de Programación (LDP135)
autor: Rickelmy Josepf Cubías Alvarado
tags:
  - python
  - sqlite
  - docker
  - doc-as-code
  - git-submodule
creado: 2026-05-15
---

#  Gestión de Inventario

![Python Version](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Database](https://img.shields.io/badge/DB-SQLite-lightgrey?logo=sqlite)
![Dev Environment|97](https://img.shields.io/badge/Env-Docker-blue?logo=docker)
![Doc Strategy](https://img.shields.io/badge/Docs-Obsidian-purple?logo=obsidian)

**Gestión de Inventario** es el motor lógico central para el control eficiente de productos, stock y movimientos de almacén, estructurado bajo una arquitectura modular estricta. El proyecto separa completamente la lógica de negocio de la interfaz de usuario, permitiendo que la aplicación opere actualmente vía CLI, con la preparación arquitectónica para evolucionar a una API REST (FastAPI) en el futuro.
---

##  Stack Tecnológico Seleccionado

| Componente | Tecnología | Justificación |
| :--- | :--- | :--- |
| **Lenguaje Core** | Python | Versatilidad y rapidez para implementar lógica de validación compleja. |
| **Persistencia** | SQLite | Base de datos incrustada que garantiza portabilidad sin configurar servidores externos. |
| **Interfaz** | CLI (Terminal) | Interfaz ligera y directa para el consumo de recursos eficiente. |
| **Despliegue** | Docker Compose | Orquestación de contenedores para asegurar un entorno idéntico en desarrollo y producción. |
| **Documentación**| Markdown | Estrategia Doc-as-Code, centralizando notas de entregas en `docs/`. |

---

##  Estructura del Repositorio

El código y la documentación se organizan siguiendo el principio de **Separación de Responsabilidades**:

```text
gestion_inventario/
│
├── core/                   #  LÓGICA DE NEGOCIO (Independiente de la CLI)
│   ├── __init__.py
│   ├── inventory.py        # Funciones de validación (ej. check_stock)
│   └── models.py           # Estructuras de datos (Clases o Diccionarios)
│
├── storage/                #  CAPA DE DATOS (Persistencia)
│   ├── __init__.py
│   ├── database.py         # Conexión a SQLite
│   └── repository.py       # Transforma filas de SQL a Diccionarios y viceversa
│
├── cli/                    #  CAPA DE PRESENTACIÓN (La interfaz actual)
│   ├── __init__.py
│   ├── menus.py            # Solo prints e inputs (interacción con el usuario)
│   └── app.py              # Conecta los inputs con el 'core'
│
├── tests/                  #  PRUEBAS UNITARIAS
│   └── test_inventory.py   # Pruebas automatizadas de reglas de negocio
│
├── docs/                   #  CENTRAL DE DOCUMENTACIÓN TÉCNICA
│   └── proyecto/
│       └── entrega_1/      # Documentos específicos de cada hito de desarrollo
│
├── main.py                 #  Punto de entrada de la aplicación
├── README.md               # Portada general del proyecto
└── .gitignore              # Excluye .obsidian/ y archivos temporales locales
```


> [!TIP] 
> 
> **Aislamiento de Entorno** 
> 
> El archivo `.gitignore` de este submódulo incluye explícitamente el directorio `.obsidian/`. Esto previene la duplicación de configuraciones con el Super Vault principal y mantiene el repositorio de la universidad limpio de archivos de configuración locales.

##  Guía de Inicio Rápido

### Desarrollo Local

1. Asegúrate de tener instalado **Python 3.10+**.
    
2. Clona este repositorio (si estás usando el Super Vault, asegúrate de inicializar los submódulos):
    
    Bash
    
    ```
    git clone --recurse-submodules [https://github.com/tu-usuario/gestion_inventario.git](https://github.com/tu-usuario/gestion_inventario.git)
    ```
    
3. Ejecuta la aplicación:
    
    Bash
    
    ```
    python main.py
    ```
    

### Despliegue con Docker

Para ejecutar el entorno aislado:

```bash
docker-compose up --build
````

---

##  Roadmap (Plan de Trabajo LDP135)

- [x] **Fase 1: Diseño de Lógica Base:** Creación de pseudocódigo en PSeInt (ver `docs/proyecto/entrega_1/`).
    
- [ ] **Fase 2: Implementación Core:** Definición de diccionarios y funciones puras en el módulo `core/`.
    
- [ ] **Fase 3: Persistencia:** Implementación del patrón repositorio sobre SQLite en `storage/`.
    
- [ ] **Fase 4: Interfaz de Usuario:** Desarrollo de la CLI interactiva y su conexión con el Core.
    
- [ ] **Fase 5: Pruebas y Despliegue:** Creación de Unit Tests y configuración final de contenedores Docker.
    

---

> [!NOTE]
> 
> Este archivo es el punto de entrada oficial para revisiones de código. Para detalles arquitectónicos, diagramas o bitácoras de decisiones, referirse al directorio `/docs/`.
