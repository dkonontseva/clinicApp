from datetime import date

from pydantic import BaseModel

from app.schemas.schemas import UserSchema


class MedicalCardResponseSchema(BaseModel):
    _id: int
    first_name: str
    last_name: str
    date: date





