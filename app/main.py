from fastapi import FastAPI, Request
from app.database import init_db
from app.routes import router
from contextlib import asynccontextmanager
from fastapi.responses import RedirectResponse
from app.middleware import redirect_undefined_routes

# Crear la aplicación FastAPI
app = FastAPI()

# Aplicar middleware antes de incluir las rutas
app.middleware("http")(redirect_undefined_routes)

# Inicializar la base de datos al inicio
@app.on_event("startup")
def on_startup():
    init_db()

# Incluir las rutas de la API
app.include_router(router)
