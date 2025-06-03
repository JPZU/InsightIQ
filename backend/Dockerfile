# Imagen base con Python
FROM python:3.11-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo
WORKDIR /app

# Copiar e instalar dependencias
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar el resto del código
COPY . .

# Exponer el puerto para FastAPI
EXPOSE 8000

# Ejecutar migraciones y luego iniciar el servidor
CMD alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000
