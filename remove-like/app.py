from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
import uvicorn

from routes.like_routes import router as like_router

# Create FastAPI app
app = FastAPI(
    title="Reactions Profile API",
    version="1.0.0",
    description="API for reactions to pet posts",
    docs_url="/api-docs-removeLike",                  
    redoc_url=None,
    openapi_url="/api-docs-likes/openapi.json",   
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(like_router)

# Customize OpenAPI schema
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

# Run app directly
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=6002, reload=True)
