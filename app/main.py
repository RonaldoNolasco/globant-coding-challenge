from fastapi import FastAPI
from app.database import init_db
from app.routes import router
from contextlib import asynccontextmanager

# Crear la aplicación FastAPI
app = FastAPI()

# Inicializar la base de datos al inicio


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 La aplicación ha iniciado")
    init_db()
    yield  # Aquí FastAPI ejecuta la aplicación
    print("🛑 La aplicación se está cerrando")

# Incluir las rutas de la API
app.include_router(router, prefix="/api")
