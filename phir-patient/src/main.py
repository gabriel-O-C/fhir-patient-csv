from fastapi import FastAPI

from .patients.router import router as patients_router

app = FastAPI()

app.include_router(patients_router)
