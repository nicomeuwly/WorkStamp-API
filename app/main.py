from fastapi import FastAPI
from .database import engine
from . import models
from .routes import users, auth
from fastapi.openapi.utils import get_openapi

app = FastAPI()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="WorkSalary API",
        version="1.0.0",
        description="API personnelle pour gérer le temps de travail et le salaire",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", []).append({"BearerAuth": []})
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

# Crée les tables au lancement de l'application
models.Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
def read_root():
    return {"message": "API en ligne ✅"}
