from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
import uvicorn

from routes.like_routes import router as like_router

# Crear la app FastAPI
app = FastAPI(
    title="Pet Profile API",
    version="1.0.0",
    description="API para el manejo de perfiles de mascotas",
    docs_url="/api-docs-addLike",                   
    redoc_url=None,
    openapi_url="/api-docs-likes/openapi.json",   
)

@app.get("/health", tags=["Health Check"])
def simple_health_check():
    return {"status": "ok"}


# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(like_router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Ejecución directa
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=6001, reload=True)
