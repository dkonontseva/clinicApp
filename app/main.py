import uvicorn
from fastapi import FastAPI

from app.api.auth.router import router as auth_router
from app.api.patients.router import router as patients_router
from app.api.doctors.router import router as doctors_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(patients_router)
app.include_router(doctors_router)