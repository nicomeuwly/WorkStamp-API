from fastapi import FastAPI
from app.routers import users
from app.routers import auth

app = FastAPI(swagger_ui_parameters={"persistAuthorization": True})

app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the WorkStamp API!"}
