# Usar una imagen base de python
FROM python:3.9-slim

# Instalar dependencias necesarias
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de requerimientos y el código
COPY requirements.txt requirements.txt
COPY app app

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Ejecutar la aplicación
CMD ["streamlit", "run", "app/main.py"]
