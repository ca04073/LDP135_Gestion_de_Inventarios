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

# Gestión de Inventario

![Python Version](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)
![HTMX](https://img.shields.io/badge/htmx-%233366cc.svg?style=flat&logo=html5&logoColor=white)
![Database](https://img.shields.io/badge/DB-SQLite-lightgrey?logo=sqlite)
![Dev Environment](https://img.shields.io/badge/Env-Docker-blue?logo=docker)
![Doc Strategy](https://img.shields.io/badge/Docs-Obsidian-purple?logo=obsidian)

**Gestión de Inventario** es el motor lógico central para el control eficiente de productos, stock y movimientos de almacén, estructurado bajo una arquitectura modular estricta. El sistema ha evolucionado de su prototipo inicial en terminal hacia una interfaz web interactiva en tiempo real (Single Page Application) utilizando un enfoque de renderizado fragmentado desde el servidor.

---

##  Stack Tecnológico Seleccionado

| Componente        | Tecnología              | Justificación                                                                                                    |
| :---------------- | :---------------------- | :--------------------------------------------------------------------------------------------------------------- |
| **Lenguaje Core** | Python                  | Versatilidad y rapidez para implementar lógica de validación compleja.                                           |
| **Persistencia**  | SQLite                  | Base de datos incrustada que garantiza portabilidad sin configurar servidores externos.                          |
| **Interfaz**      | CLI (Terminal)          | Interfaz ligera y directa para el consumo de recursos eficiente.                                                 |
| **Despliegue**    | Docker Compose          | Orquestación de contenedores para asegurar un entorno idéntico en desarrollo y producción.                       |
| **Documentación** | Markdown                | Estrategia Doc-as-Code, centralizando notas de entregas en `docs/`.                                              |
| **Interfaz**      | Web UI (FastAPI + HTMX) | Interfaz asíncrona reactiva que renderiza componentes en el servidor sin sobrecarga de JavaScript en el cliente. |

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
    
- [x] **Fase 2: Implementación Core:** Definición de diccionarios y funciones puras en el módulo `core/`.
    
- [x] **Fase 3: Persistencia:** Implementación del patrón repositorio sobre SQLite en `storage/`.
    
- [x] **Fase 4: Interfaz de Usuario:** Desarrollo de la CLI interactiva y su conexión con el Core.
    
- [x] **Fase 5: Pruebas y Despliegue:** Creación de Unit Tests y configuración final de contenedores Docker.
    

---

> [!NOTE]
> 
> Este archivo es el punto de entrada oficial para revisiones de código. Para detalles arquitectónicos, diagramas o bitácoras de decisiones, referirse al directorio `/docs/`.

## 🌐 Fase 3: Interfaz Web Reactiva e Infraestructura Contenedorizada (Completado)

Se migró la capa de presentación desde la interfaz de línea de comandos (CLI) hacia una **Single Page Application (SPA)** reactiva de alto rendimiento utilizando **FastAPI** y **HTMX**, eliminando la sobrecarga de frameworks JavaScript pesados. El sistema incluye un pipeline de integración continua y un empaquetado profesional listo para producción.

### 🛠️ Stack Tecnológico de Infraestructura
* **Backend:** FastAPI (Python 3.10-alpine) para la API asíncrona [diseno_web_infra.md].
* **Frontend:** HTMX para la reactividad mediante renderizado de fragmentos HTML en el servidor, estilizado con Tailwind CSS dinámico [diseno_web_infra.md].
* **Persistencia:** Base de datos SQLite integrada mediante volumen persistente [diseno_web_infra.md].
* **Orquestación y CI/CD:** Docker, Docker Compose y GitHub Actions (`ghcr.io`) [diseno_web_infra.md].

---

### 🚀 Instrucciones de Despliegue Rápido (Producción)

Para levantar el sistema de inventario de forma local o en un servidor sin necesidad de configurar entornos virtuales de Python ni dependencias manuales, ejecuta los siguientes comandos en tu terminal:

1. **Clonar el repositorio y moverse a la carpeta:**

```bash
git clone [https://github.com/ca04073/LDP135_Gestion_de_Inventarios.git](https://github.com/ca04073/LDP135_Gestion_de_Inventarios.git) cd LDP135_Gestion_de_Inventarios
```

2. Levantar el entorno contenedorizado con Docker Compose:

```bash
docker compose up -d --build
```

3. **Acceder a la aplicación:**

	Si estás en local: 
	
- **Interfaz Web del Inventario:** Abre tu navegador en `http://localhost:8000` (o la IP de tu servidor Proxmox).
    
- **Documentación Interactiva de la API (Swagger UI):** Accede a `http://localhost:8000/docs`.

	Si estas en despliegue remoto, usa tu url de acceso, por ejemplo:
		**inventario.mi-dominio.com**
		

### 🛡️ Características Robustecidas de Grado Profesional

- **Manejo de Errores Asíncrono:** Control semántico de errores mediante estados HTTP 400 Bad Request interceptados en caliente por eventos de HTMX (`before-swap`) para inyección dinámica de alertas en el DOM sin recargas de página [diseno_web_infra.md].
    
- **Aislamiento e Inmutabilidad:** La base de datos se almacena en un volumen mapeado local (`./data`), lo que garantiza que los registros de inventario sean indestructibles ante actualizaciones o reinicios del contenedor [diseno_web_infra.md].
    
- **Seguridad del Repositorio:** Reglas de protección activadas en la rama `main` que impiden pushes directos, obligando al uso de Pull Requests auditados por el pipeline automático de Actions [diseno_web_infra.md].