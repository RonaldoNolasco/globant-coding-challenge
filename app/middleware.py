from fastapi import Request
from fastapi.responses import RedirectResponse

# Se define una ruta por defecto a la cual se redirige en caso de acceder a rutas no existentes
async def redirect_undefined_routes(request: Request, call_next):
    response = await call_next(request)
    if response.status_code == 404:
        return RedirectResponse(url="/docs")
    return response
