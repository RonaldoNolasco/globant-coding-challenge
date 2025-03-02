# Usa una imagen base ligera de Python
FROM python:3.11-slim-buster

# Define el directorio de trabajo dentro del contenedor
WORKDIR /usr/src/app

# Configura variables de entorno para mejorar rendimiento de Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instala dependencias del sistema
RUN apt-get update \
  && apt-get -y install netcat gcc postgresql-client \
  && apt-get clean

# Copia el archivo de dependencias e instálalas
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copia todo el código de la app
COPY . .

# Expone el puerto de la aplicación
EXPOSE 8000

# Comando por defecto para ejecutar FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
