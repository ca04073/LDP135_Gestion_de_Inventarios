### 🧱 1. Modularidad Estricta (Arquitectura Desacoplada)

- **Independencia del Núcleo:** El sistema se rige bajo una filosofía de separación de responsabilidades, donde el núcleo del negocio (`core/`) no sabe ni le importa cómo se muestran los datos ni dónde se guardan.
    
- **Adaptadores Intercambiables:** Gracias a este aislamiento, la migración de la interfaz de consola (CLI) a la interfaz Web (FastAPI + HTMX) se realizó de forma quirúrgica, sustituyendo el controlador de entrada sin modificar una sola línea de la lógica de inventario.
    
- **Preparado para el Futuro:** Esta misma modularidad es la que te permite proyectar a largo plazo una evolución del backend hacia microservicios especializados (como separar la concurrencia en Go y el procesamiento crítico en Rust) sin romper la estructura general.
    

### 🗃️ 2. El Patrón Repositorio (Abstracción de Persistencia)

- **Aislamiento de la Base de Datos:** El `core` nunca habla directamente con la base de datos. Toda interacción se realiza a través de una interfaz intermedia (`storage/`).
    
- **Flexibilidad de Almacenamiento:** Actualmente el sistema consume **libSQL/SQLite** de manera local. Sin embargo, gracias al patrón repositorio, migrar todo el sistema hacia una base de datos relacional robusta como **PostgreSQL** es tan sencillo como cambiar el adaptador de conexión y las consultas SQL en un solo módulo, manteniendo el resto del software intacto.
    
- **Seguridad en Pruebas:** Permite aislar los datos de producción de los entornos de prueba, garantizando que los tests unitarios verifiquen la corrección lógica sin ensuciar el archivo físico de persistencia.
    

### 🛡️ 3. Gestión de Errores Asíncrona y Semántica Web

- **Cláusulas de Guarda en el Core:** El núcleo del negocio valida de forma estricta las reglas (evitando precios o stocks negativos) lanzando excepciones nativas `ValueError`.
    
- **Semántica HTTP Robusta:** FastAPI intercepta estos fallos y los traduce automáticamente en estados **HTTP 400 Bad Request**, pre-renderizando un fragmento UI de alerta estilizado con Tailwind CSS en lugar de romper el hilo de ejecución del servidor.
    
- **Reactividad Eficiente con HTMX:** En el cliente, un interceptor en caliente (`before-swap`) captura los códigos `400` y desvía de forma dinámica el DOM del navegador para inyectar la alerta roja exactamente arriba del formulario, ofreciendo una experiencia reactiva de Single Page Application sin necesidad de recargar la página.
    

### 🚀 El "Plus" de Infraestructura (CI/CD y DevOps)

- **Contenerización Ligera:** Empaquetado optimizado en **Docker** bajo imágenes `python:3.10-alpine` (menores a 100MB) con persistencia indestructible mediante volúmenes enlazados.
    
- **Automatización y Blindaje:** Pipeline automatizado en **GitHub Actions** hacia `ghcr.io` acoplado a **reglas de protección de ramas**, bloqueando pushes directos a `main` y obligando a un flujo de trabajo profesional por Pull Requests validados en la nube.