from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr

from app.schemas.schemas import BaseSchema, UserSchema, AddressSchema, DepartmentSchema, EducationSchema


class DoctorResponseSchema(BaseModel):
    _id: int
    start_date: date
    birthday: date
    users: UserSchema
    addresses: AddressSchema
    departments: DepartmentSchema


# class UserUpdateSchema(BaseModel):
#     login: Optional[EmailStr] = None
#     password: Optional[str] = None
#     first_name: Optional[str] = None
#     last_name: Optional[str] = None
#     second_name: Optional[str] = None
#     phone_number: Optional[str] = None
#     gender: Optional[str] = None
#     role_id: Optional[int] = None
#
#
# class AddressUpdateSchema(BaseModel):
#     country: Optional[str] = None
#     city: Optional[str] = None
#     street: Optional[str] = None
#     house_number: Optional[str] = None
#     flat_number: Optional[int] = None

class DoctorUpdateSchema(BaseSchema):
    start_date: Optional[date]
    birthday: Optional[date]
    department_id: Optional[int]
    users: Optional[UserSchema]
    addresses: Optional[AddressSchema]
    education: Optional[EducationSchema]