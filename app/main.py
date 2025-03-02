from fastapi import FastAPI
from app.database import init_db
from app.routes import router
from contextlib import asynccontextmanager
from fastapi.responses import RedirectResponse

# Crear la aplicación FastAPI
app = FastAPI()

@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")

# Inicializar la base de datos al inicio
@app.on_event("startup")
def on_startup():
    init_db()

# Incluir las rutas de la API
app.include_router(router)
