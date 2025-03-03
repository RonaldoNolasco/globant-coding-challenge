# Globant Data Engineering Coding Challenge

## Descripción
Este proyecto es una solución desarrollada para el Data Engineering Coding Challenge de Globant. Se ha construido una API REST que permite la migración de datos históricos desde archivos CSV a una base de datos SQL, cumpliendo con los requisitos establecidos en el challenge.

## Contenido
- [Globant Data Engineering Coding Challenge](#globant-data-engineering-coding-challenge)
  - [Descripción](#descripción)
  - [Contenido](#contenido)
  - [Tecnologías Utilizadas](#tecnologías-utilizadas)
  - [Estructura del Proyecto](#estructura-del-proyecto)
  - [Instalación y Configuración](#instalación-y-configuración)
    - [1. Clonar el repositorio](#1-clonar-el-repositorio)
    - [2. Crear y activar un entorno virtual](#2-crear-y-activar-un-entorno-virtual)
    - [3. Instalar dependencias](#3-instalar-dependencias)
    - [4. Configurar variables de entorno](#4-configurar-variables-de-entorno)
    - [5. Ejecutar la API](#5-ejecutar-la-api)
  - [Uso de la API](#uso-de-la-api)
  - [Sección 1: API](#sección-1-api)
    - [Endpoints Disponibles](#endpoints-disponibles)
  - [Sección 2: SQL](#sección-2-sql)
  - [Bonus Track: Cloud, Testing \& Containers](#bonus-track-cloud-testing--containers)
    - [**Cloud Deployment**](#cloud-deployment)
    - [**Testing**](#testing)
    - [**Docker**](#docker)
  - [Imágenes del Proyecto](#imágenes-del-proyecto)

## Tecnologías Utilizadas
- **Python 3.10.13** (Lenguaje de programacion principal)
- **FastAPI** (Framework para la API REST)
- **SQLModel** (ORM para interacción con la base de datos)
- **SQLite** (Base de datos utilizada para desarrollo y pruebas)
- **PostgreSQL** (Base de datos utilizada en producción)
- **Docker** (Containerización)
- **Pytest** (Testing automatizado)
- **Railway.com** (Plataforma de despliegue en la nube)

## Estructura del Proyecto
```plaintext
├── app/
│   ├── main.py        # Punto de entrada de la API
│   ├── routes.py      # Definición de rutas de la API
│   ├── database.py    # Configuración de la base de datos
│   ├── models.py      # Modelos de la base de datos
│   ├── services.py    # Lógica de negocio
│   ├── utils.py       # Funciones auxiliares
│   ├── middleware.py  # Manejo de errores
│   ├── constants.py   # Constantes del proyecto
├── data/              # Carpeta de datos de entrada
│   ├── departments/   # Datos de los departamentos
│   ├── employees/     # Datos de los empleados
│   ├── jobs/          # Datos de los trabajos
├── tests/             # Pruebas automatizadas
│   ├── config.py      # Configuracion para las pruebas
│   ├── test_api.py    # Pruebas a los endpoints de la API
│   ├── test_crud.py   # Pruebas al CRUD de las entidades
├── Dockerfile         # Configuración del contenedor
├── docker-compose.yml # Configuración de Docker Compose
├── requirements.txt   # Dependencias del proyecto
├── .env               # Variables de entorno
├── .env.test          # Variables de entorno para pruebas
├── .gitignore         # Archivos ignorados en el repositorio
├── pytest.ini         # Configuración de pytest
├── README.md          # Documentación
```

## Instalación y Configuración
### 1. Clonar el repositorio
```bash
 git clone https://github.com/tu-usuario/nombre-repositorio.git
 cd nombre-repositorio
```
### 2. Crear y activar un entorno virtual
```bash
 python -m venv .venv
 source .venv\Scripts\activate  # En Linux/Mac: source .venv/bin/activate
```
### 3. Instalar dependencias
```bash
 python -m pip install -r requirements.txt
```
### 4. Configurar variables de entorno
Crear un archivo `.env` y definir la variable `DATABASE_URL`:
```env
DATABASE_URL=sqlite:///db/database.db  # Para desarrollo y pruebas
# DATABASE_URL=postgresql://user:password@host:port/dbname  # Para producción
```
### 5. Ejecutar la API
```bash
 python -m fastapi dev app/main.py
```
La API estará disponible en `http://localhost:8000`.

## Uso de la API
La documentación interactiva se puede acceder en:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

## Sección 1: API
La API proporciona endpoints para recibir y procesar archivos CSV con datos de empleados, departamentos y trabajos.

### Endpoints Disponibles
- **Carga de CSVs:**
  - `POST /upload/departments/`
  - `POST /upload/jobs/`
  - `POST /upload/employees/`
- **Consulta de datos:**
  - `GET /employees_per_quarter/` (Empleados contratados por trimestre en 2021)
  - `GET /departments_above_mean/` (Departamentos con contrataciones por encima de la media en 2021)


Ejemplo de petición POST:
```bash
 curl -X POST "http://127.0.0.1:8000/upload/employees/" -F "file=@hired_employees.csv"
```

Ejemplo de petición GET:
```bash
 curl -X GET "http://localhost:8000/employees_per_quarter/"
```

## Sección 2: SQL
Se han desarrollado consultas para extraer información clave de la base de datos.

1. **Cantidad de empleados contratados por trimestre en 2021**
2. **Departamentos que contrataron más empleados que la media**

Ejemplo de respuesta esperada para la consulta 1:
```json
[
  {"department": "Staff", "job": "Recruiter", "Q1": 3, "Q2": 2, "Q3": 0, "Q4": 0}
]
```

Ejemplo de respuesta esperada para la consulta 2:
```json
[
  {"id": 1, "department": "Engineering", "hired": 150},
  {"id": 2, "department": "Marketing", "hired": 90}
]
```

## Bonus Track: Cloud, Testing & Containers
### **Cloud Deployment**
La aplicación se encuentra desplegada en **Railway.com**, donde se ejecuta el contenedor de la API junto con la base de datos PostgreSQL.

### **Testing**
Se han implementado tests automáticos con `pytest` para validar la funcionalidad de la API.

Ejecutar tests:
```bash
 pytest test/test_api.py  # Para pruebas de API
 pytest test/test_crud.py  # Para pruebas de CRUD
```

### **Docker**
Para ejecutar la aplicación en un contenedor Docker:
```bash
 docker build -t my-fastapi-app .
 docker run -p 8000:8000 my-fastapi-app
```

## Imágenes del Proyecto
_Agregar capturas de pantalla o diagramas aquí_

---
Este proyecto fue desarrollado aplicando las mejores prácticas de desarrollo, incluyendo modularidad, pruebas y despliegue en la nube.

