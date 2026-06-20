---
proyecto: Gestión de Inventario
etapa: 3 - Interfaz Web e Infraestructura de Despliegue (Entrega 3)
materia: Lógica de Programación (LDP135)
estado: Completado
tags:
  - fastapi
  - htmx
  - tailwind-css
  - ssr
  - renderizado-fragmentado
  - docker
  - proxmox
creado: 2026-06-13
---

# 🌐 Interfaz Web Reactiva e Infraestructura de Despliegue Contenedorizada

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi) ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white) ![HTMX](https://img.shields.io/badge/htmx-%233366cc.svg?style=for-the-badge&logo=html5&logoColor=white) ![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white) ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white) ![Proxmox](https://img.shields.io/badge/Proxmox-E74C3C?style=for-the-badge&logo=proxmox&logoColor=white)  

Este documento detalla las decisiones arquitectónicas y tecnológicas aplicadas para la Fase 3 del proyecto **Gestión de Inventario**. Especifica la migración de la capa de presentación hacia un entorno web asíncrono y la estrategia de empaquetado para su despliegue en infraestructura local.

---

## ⚖️ Justificación de la Capa Web: FastAPI + HTMX

En lugar de adoptar la sobrecarga de frameworks SPA tradicionales basados en JavaScript pesado (como Next.js y React), se optó por un enfoque arquitectónico minimalista y de alto rendimiento basado en **FastAPI** y **HTMX**. 

### 1. Reactividad sin JavaScript Complicado (Filosofía Hyper-Práctica)
HTMX permite al navegador realizar peticiones AJAX directamente mediante atributos HTML declarativos (`hx-post`, `hx-delete`). El servidor FastAPI no responde con pesados archivos JSON que el cliente deba procesar; en su lugar, devuelve pequeños trozos de HTML pre-renderizados (componentes) que HTMX inyecta en el DOM en tiempo real sin recargar la página.

### 2. Preservación Absoluta del Núcleo (Arquitectura Hexagonal)
Gracias al aislamiento arquitectónico implementado en la Fase 2, la integración de la interfaz web se realizó sin modificar una sola línea de código del núcleo del negocio (`core/`) o de la capa de persistencia (`storage/`). El módulo `web/app.py` funciona simplemente como un nuevo adaptador de entrada (Controller) que sustituye por completo a la CLI (`cli/menus.py`).

> [!IMPORTANT]
> 
> **Manejo Estricto de Tipos MIME en Entornos de Red**
> 
> Durante la fase de integración en servidores locales, se incorporó el módulo nativo `mimetypes` en el núcleo de FastAPI. Esto blinda la compatibilidad del sistema asegurando que los archivos estáticos de configuración `.js` sean interpretados bajo la cabecera exacta `application/javascript`, evitando bloqueos de seguridad por parte del navegador.

---

## 🎨 Arquitectura de Estilos y Sistema de "Theming" Dinámico

El diseño visual se construyó utilizando **Tailwind CSS** acoplado a un motor de plantillas **Jinja2**. Para evitar la rigidez estética y cumplir con principios de mantenibilidad profesional, se diseñó un sistema de personalización centralizado:

### 1. Configuración Inyectada en Caliente
Para mitigar la sobrecarga de dependencias de Node.js en entornos de desarrollo restringidos, la paleta de colores corporativa se centralizó en la cabecera (`<head>`) del archivo base `index.html` extendiendo el objeto nativo global `tailwind.config`.

### 2. Abstracción por Variables de Intercambio 
Todos los componentes visuales (`index.html` y `filas_tabla.html`) consumen alias lógicos (`text-brand-claro`, `bg-brand-base`, `hover:bg-brand-oscuro`) en lugar de colores fijos. Esto permite alternar la identidad visual completa del software (como el paso del Verde Esmeralda al Morado o al que se elija según la necesidad) modificando exclusivamente tres variables hexadecimales en un único punto del código.

```text
[Ajuste de Hexadecimales en index.html] 
                  │
                  ▼ (Hereda automáticamente)
[Clases semánticas: brand-claro / brand-base]
                  │
                  ├─► Componente del Formulario
                  └─► Componente de Filas de la Tabla (filas_tabla.html)
````

## 🛠️ Especificación de Endpoints y Flujo de Datos (CRUD Web)

La API asíncrona expone un flujo cerrado de operaciones interactivas que mapean directamente las capacidades del Core:

- **`GET /` (index):** Carga inicial de la Single Page Application (SPA). Consume `inventory.consultar_inventario()` y renderiza la estructura completa inyectando el estado actual de la base de datos SQLite.
    
- **`GET /productos/tabla`:** Endpoint interno que renderiza única y exclusivamente el componente fragmentado `filas_tabla.html`. Es el objetivo principal de recarga para HTMX.
    
- **`POST /productos`:** Recibe datos estructurados de formularios (`application/x-www-form-urlencoded`) mediante el validador `python-multipart`. Ejecuta la inserción en el Core y, tras el éxito, delega la respuesta al renderizador de la tabla para actualizar la UI sin parpadeos.
    
- **`POST /productos/actualizar`:** Procesa la mutación controlada del registro. Bloquea la edición de la clave primaria (`codigo`) mediante estados de solo lectura en el cliente y actualiza el resto de campos en caliente.
    
- **`DELETE /productos/{codigo}`:** Remueve el registro físico de la base de datos. Al responder con un cuerpo de texto vacío (`""`) acoplado a la estrategia `hx-swap="outerHTML"`, HTMX elimina de forma inmediata y automática la fila correspondiente del DOM del navegador.
    

## 🛡️ Protocolo Robustecido de Manejo de Errores y Estados HTTP

La migración hacia un entorno Web/API requirió transformar el modelo de excepciones tradicional (capturas síncronas en consola) hacia un **Flujo de Control de Errores Asíncrono** basado en semántica HTTP y manipulación selectiva del DOM vía HTMX.

### 1. Capa de Backend (FastAPI): Semántica de Estados
Cuando el núcleo del negocio (`core/inventory.py`) intercepta una violación a las cláusulas de guarda (como un intento de registrar un precio o stock negativo), lanza una excepción nativa `ValueError` [diseno_backend.md]. El adaptador web captura esta excepción y, en lugar de romper el hilo de ejecución o devolver una estructura de datos rota, emite una respuesta web controlada:
* **Código de Estado HTTP 400 (Bad Request):** Indica explícitamente al cliente que la petición falló debido a datos inválidos.
* **Encapsulamiento UI:** El mensaje del error es pre-renderizado en el servidor dentro de un fragmento HTML estilizado con Tailwind CSS de forma nativa (clases `bg-red-900/50` y `text-red-200`).

### 2. Capa de Frontend (HTMX): Intercepción de Eventos del Ciclo de Vida
Por defecto, HTMX ignora o no renderiza respuestas que viajen con códigos de estado de error (`4xx` o `5xx`). Para resolver esto de manera elegante en la Single Page Application sin recargar la página, se implementó un interceptor en caliente utilizando el evento nativo `hx-on::before-swap`:

```html
hx-on::before-swap="if(event.detail.xhr.status === 400) { event.detail.target = htmx.find('#alerta-error'); event.detail.shouldSwap = true; }"
````

- **Flujo Exitoso (HTTP 200 OK):** La respuesta contiene las filas actualizadas (`filas_tabla.html`) y se inyecta directamente en el cuerpo principal de la tabla (`#tabla-productos`) [diseno_web_infra.md].
    
- **Flujo Fallido (HTTP 400 Bad Request):** El evento intercepta la respuesta antes del intercambio, desvía el objetivo dinámicamente hacia un contenedor dedicado a notificaciones (`#alerta-error`) y fuerza la inyección de la alerta de error.
    

Esto garantiza un sistema tolerante a fallos, previene estados inconsistentes en la base de datos SQLite y ofrece una experiencia de usuario limpia, donde las alertas reactivas aparecen en pantalla de forma instantánea sin interrumpir la persistencia del inventario [diseno_backend.md, diseno_web_infra.md].

## 🐳 Estrategia de Infraestructura y Despliegue (Docker + Proxmox)

Para garantizar la portabilidad y optimizar el rendimiento en servidores con recursos de hardware modestos o antiguos, se diseñó una infraestructura basada en la virtualización ligera:

Plaintext

```
 ┌────────────────────────────────────────────────────────┐
 │                   SERVIDOR PROXMOX                     │
 │  ┌──────────────────────────────────────────────────┐  │
 │  │                 CONTENEDOR LXC                   │  │
 │  │  ┌────────────────────────────────────────────┐  │  │
 │  │  │              ENTORNO DOCKER                │  │  │
 │  │  │  [FastAPI App Web] ◄──► [Volumen SQLite]   │  │  │
 │  │  └────────────────────────────────────────────┘  │  │
 │  └──────────────────────────────────────────────────┘  │
 └────────────────────────────────────────────────────────┘
```

### 1. Encapsulamiento Ultraligero (Dockerfile)

Se utiliza una imagen base de **Python Alpine**, reduciendo el tamaño total del contenedor a menos de 100MB. El contenedor expone el puerto nativo `8000` y delega la ejecución al servidor de grado de producción `uvicorn`.

### 2. Orquestación y Persistencia (Docker Compose)

Dado que SQLite opera sobre un único archivo local (`inventario.db`), reiniciar un contenedor destruiría el historial académico de datos. Para solucionar esto, el orquestador `docker-compose.yml` monta un **Volumen de Datos Externo**, enlazando el archivo de la base de datos con el almacenamiento físico del sistema anfitrión, garantizando la persistencia indestructible de la información.

### 3. Alojamiento en Contenedores LXC (Proxmox Virtual Environment)

En lugar de instanciar Máquinas Virtuales completas con sobrecarga de hardware, el proyecto se despliega dentro de un **Contenedor Linux (LXC)**. Al compartir de forma directa el núcleo del servidor físico, el consumo de memoria RAM y CPU se reduce al mínimo absoluto, permitiendo una ejecución fluida incluso en procesadores de generaciones anteriores.

## 🚀 Fase de Despliegue e Infraestructura Automatizada (CI/CD)

El proceso de despliegue fue robustecido mediante un pipeline de Integración Continua (GitHub Actions) y Orquestación de Contenedores (Docker Compose), logrando un entorno de producción aislado e independiente del entorno de desarrollo.

1. **Compilación en la Nube:** Cada actualización sobre la rama de seguimiento `CA04073/docker-deployment` dispara una compilación automatizada que empaqueta la aplicación basada en Python Alpine, garantizando un binario de tamaño optimizado y libre de dependencias rotas.
2. **Registro Privado:** Las imágenes validadas son almacenadas con etiquetas de control (`:latest` y `:sha`) en el GitHub Container Registry (ghcr.io), protegidas bajo autenticación de llaves securizadas (PAT).
3. **Despliegue Desacoplado:** El servidor privado (Proxmox) descarga y ejecuta de forma directa el paquete remoto a través de un archivo `docker-compose.yml` optimizado, exponiendo el servicio en el puerto web estándar (HTTP 80) y asegurando la persistencia inmutable de la base de datos SQLite en el volumen local `./data`.