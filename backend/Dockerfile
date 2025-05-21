# Imagen base ligera de Python
FROM python:3.11-slim

# Establecer variable de entorno para evitar buffering
ENV PYTHONUNBUFFERED=1

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para compilación de algunas librerías (como pandas, openpyxl, mysqlclient, etc.)
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    libssl-dev \
    libmariadb-dev\
    libmariadb-dev-compat\
    build-essential \
    python3-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias del proyecto
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Exponer el puerto por donde correrá FastAPI
EXPOSE 8000

# Comando para correr el servidor (modo desarrollo)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
