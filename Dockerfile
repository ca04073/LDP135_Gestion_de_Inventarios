# 1. Usamos una imagen oficial de Python basada en Alpine Linux (Ultra ligera)
FROM python:3.10-alpine

# 2. Definimos el directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiamos el archivo de dependencias primero (Optimiza el caché de Docker)
COPY requirements.txt .

# 4. Instala las dependencias de Python dentro del entorno aislado
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiamos todo el código fuente de nuestra aplicación al contenedor
COPY . .

# 6. Exponemos el puerto nativo en el que corre FastAPI
EXPOSE 8000

# 7. Comando de ejecución usando Uvicorn apuntando a tu app web
CMD ["uvicorn", "web.app:app", "--host", "0.0.0.0", "--port", "8000"]