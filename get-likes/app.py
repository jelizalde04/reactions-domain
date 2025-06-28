from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
import uvicorn
import strawberry.fastapi
from schemas.graphql_schema import schema

from routes.like_routes import router as like_router


# Crear la app FastAPI
app = FastAPI(
    title="Reactions API",
    version="1.0.0",
    description="API for reactions to pet posts",
    docs_url="/api-docs-getLikes",                  
    redoc_url=None,
    openapi_url="/api-docs-getLikes/openapi.json",   
)

graphql_app = strawberry.fastapi.GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql", include_in_schema=False)


# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir las rutas
app.include_router(like_router)

# Customizar el esquema OpenAPI (opcional, solo si quieres personalizarlo)
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
    uvicorn.run("app:app", host="0.0.0.0", port=6003, reload=True)
