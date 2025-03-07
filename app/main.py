import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth.router import router as auth_router
from app.api.patients.router import router as patients_router
from app.api.doctors.router import router as doctors_router
from app.api.medical_cards.router import router as medcard_router
from app.api.doctor_leaves.router import router as leaves_router
from app.api.schedule.router import router as schedule_router
from app.api.talons.router import router as talons_router
from app.api.chat.router_socket import router as chat_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешает все источники, можно заменить на нужные
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(patients_router)
app.include_router(doctors_router)
app.include_router(medcard_router)
app.include_router(leaves_router)
app.include_router(schedule_router)
app.include_router(talons_router)
app.include_router(chat_router)


# поиск и фильтрация, функции для админа для добавления всех сущностей, чат, печать выписок из карты, ии ассистент
