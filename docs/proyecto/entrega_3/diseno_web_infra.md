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
Políticas de desacoplamiento estricto permitieron que la integración de la interfaz web se realizara sin modificar una sola línea de código del núcleo del negocio (`core/`) o de la capa de persistencia (`storage/`). El módulo `web/app.py` funciona simplemente como un nuevo adaptador de entrada (Controller) que sustituye por completo a la interfaz de consola.

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
Todos los componentes visuales (`index.html` y `filas_tabla.html`) consumen alias lógicos (`text-brand-claro`, `bg-brand-base`, `hover:bg-brand-oscuro`) en lugar de colores fijos. Esto permite alternar la identidad visual completa del software modificando exclusivamente tres variables hexadecimales en un único punto del código.

```text
[Ajuste de Hexadecimales in index.html] 
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
    

## 🛡️ Protocolo de Manejo de Errores y Estados HTTP en la Web

La migración hacia un entorno Web/API requirió transformar el modelo de excepciones tradicional hacia un **Flujo de Control de Errores Asíncrono** basado en semántica HTTP y la manipulación selectiva del DOM mediante HTMX.

### 1. Backend (FastAPI): Semántica de Estados y Cláusulas de Guarda

Cuando el núcleo del negocio (`core/inventory.py`) intercepta una violación a las reglas (como stock o precios negativos), lanza una excepción nativa `ValueError`. El adaptador web captura esta excepción y emite una respuesta web controlada:

- **HTTP 400 Bad Request:** Indica explícitamente al cliente que la petición falló debido a datos inválidos.
    
- **Fragmento UI Pre-renderizado:** El mensaje del error es encapsulado directamente en un componente HTML de alerta estilizado con Tailwind CSS de forma nativa utilizando las clases `bg-red-900/50` y `text-red-200`.
    

### 2. Frontend (HTMX): Intercepción del Ciclo de Vida y Desvío del DOM

Por defecto, HTMX ignora o no renderiza respuestas que viajen con códigos de estado de error (`4xx`). Para solucionar esto de manera reactiva en la Single Page Application sin recargar la página, se implementó un interceptor utilizando el evento nativo `hx-on::before-swap`:

HTML

```
hx-on::before-swap="if(event.detail.xhr.status === 400) { event.detail.target = htmx.find('#alerta-error'); event.detail.shouldSwap = true; }"
```

- **Flujo Exitoso (HTTP 200 OK):** La respuesta inyecta las filas actualizadas (`filas_tabla.html`) directamente en el cuerpo principal de la tabla (`#tabla-productos`).
    
- **Flujo Fallido (HTTP 400 Bad Request):** El evento intercepta la respuesta antes del intercambio, desvía el objetivo dinámicamente hacia el contenedor dedicado a notificaciones (`#alerta-error`) y fuerza la inyección de la alerta de error.
    

Esto garantiza un sistema tolerante a fallos, previene estados inconsistentes en la base de datos SQLite y ofrece una experiencia de usuario limpia, donde las alertas reactivas aparecen en pantalla de forma instantánea sin interrumpir la persistencia del inventario.

## 🐳 Estrategia de Infraestructura y Despliegue (Docker + Proxmox)

Para garantizar la portabilidad y optimizar el rendimiento en servidores con recursos de hardware modestos o antiguos, se diseñó una infraestructura basada en la virtualización ligera:

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

Se utiliza una imagen base oficial de **Python Alpine**, reduciendo el tamaño total del contenedor a menos de 100MB. El entorno expone el puerto nativo `8000` y delega la ejecución al servidor de grado de producción `uvicorn`.

### 2. Orquestación Desacoplada y Persistencia (Docker Compose)

Para el entorno del servidor de producción, se implementó un archivo `docker-compose.yml` optimizado que elimina las dependencias de compilación local (`build:`).

- **Persistencia Indestructible:** Dado que SQLite opera sobre un archivo local (`inventario.db`), el orquestador monta un volumen externo (`./data:/app/data`), enlazando el almacenamiento del contenedor con el disco físico del host anfitrión para prevenir pérdidas de datos durante actualizaciones.
    
- **Optimización de Puertos:** Se mapea el puerto web estándar HTTP `80` del servidor hacia el `8000` interno del contenedor, permitiendo el ingreso directo a la plataforma desde la red local mediante la IP del host sin declarar sufijos de puerto en el navegador.
    

### 3. Alojamiento Eficiente en Contenedores LXC (Proxmox VE)

En lugar de instanciar Máquinas Virtuales con sobrecarga de hardware, el entorno Docker se despliega dentro de un **Contenedor Linux (LXC)** en Proxmox. Al compartir directamente el núcleo del servidor físico, el consumo de memoria RAM y CPU se reduce al mínimo absoluto, permitiendo una ejecución fluida incluso en procesadores de generaciones anteriores.

## 🚀 Infraestructura Automatizada y Pipeline de Despliegue (CI/CD)

El proceso de empaquetado y puesta en marcha final del sistema fue robustecido mediante un pipeline de Integración Continua (GitHub Actions) enlazado al control de acceso por carnet del repositorio (`CA04073/docker-deployment`).

1. **Compilación Automatizada en la Nube:** Cada actualización sobre el repositorio dispara un flujo de trabajo que compila de forma aislada la receta del `Dockerfile`, garantizando un artefacto limpio y libre de dependencias rotas del entorno de desarrollo.
    
2. **Registro de Paquetes (GitHub Container Registry):** Las imágenes validadas se almacenan de forma segura bajo etiquetas de control de versiones (`:latest` y el `:sha` único del commit de Git) en el dominio privado de `ghcr.io`, protegidas mediante tokens de acceso personal clásicos (PAT) con permisos explícitos de lectura.
    
3. **Flujo de Trabajo Blindado (Branch Protection):** Se incorporaron reglas estrictas de protección en la rama `main` que impiden los pushes directos en la terminal. El sistema obliga a interactuar a través de Pull Requests (PR) auditados y requiere de forma obligatoria que el estado del pipeline de Actions termine en verde antes de habilitar la fusión del código a la rama principal.