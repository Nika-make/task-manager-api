from app.database import Base, engine
from app import models
from fastapi import FastAPI
from app.routes import auth, tasks

Base.metadata.create_all(bind=engine)



app= FastAPI()

# Incluiremos las rutas
app.include_router(tasks.router)
app.include_router(auth.router)


@app.get("/")
def home():
    return "hola mundo"