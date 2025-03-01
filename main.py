from fastapi import FastAPI
from app.database import init_db
from app.routes import router

# Crear la aplicación FastAPI
app = FastAPI()

# Inicializar la base de datos al inicio
@app.on_event("startup")
def startup():
    init_db()

# Incluir las rutas de la API
app.include_router(router, prefix="/api")
