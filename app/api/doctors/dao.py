from fastapi import HTTPException
from sqlalchemy import select, delete, update
from sqlalchemy.orm import contains_eager, joinedload

from app.api.auth.auth import get_password_hash
from app.api.dao import BaseDAO
from app.api.doctors.schemas import DoctorUpdateSchema
from app.core.database import async_session_maker
from app.models.models import Users, Addresses, Doctors, Education


class DoctorsDAO(BaseDAO):
    model = Doctors

    @classmethod
    async def get_full_data(cls):
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .options(joinedload(cls.model.users), joinedload(cls.model.addresses),
                         joinedload(cls.model.departments), joinedload(cls.model.education))
            )
            result = await session.execute(query)
            return result.scalars().all()


    @classmethod
    async def get_by_id(cls, doctor_id: int):
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .options(joinedload(cls.model.users), joinedload(cls.model.addresses),
                         joinedload(cls.model.departments), joinedload(cls.model.education))
                .filter_by(_id=doctor_id)
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def add_doctor(cls, doctor_data: DoctorUpdateSchema):
        async with async_session_maker() as session:
            async with session.begin():
                new_user = Users(
                    login=doctor_data.users.login,
                    password=get_password_hash(doctor_data.users.password),
                    first_name=doctor_data.users.first_name,
                    last_name=doctor_data.users.last_name,
                    second_name=doctor_data.users.second_name,
                    phone_number=doctor_data.users.phone_number,
                    gender=doctor_data.users.gender,
                    role_id=2
                )
                session.add(new_user)
                await session.flush()

                new_address = Addresses(
                    country=doctor_data.addresses.country,
                    city=doctor_data.addresses.city,
                    street=doctor_data.addresses.street,
                    house_number=doctor_data.addresses.house_number,
                    flat_number=str(doctor_data.addresses.flat_number)
                )
                session.add(new_address)
                await session.flush()

                new_education = Education(
                    university=doctor_data.education.university,
                    faculty=doctor_data.education.faculty,
                    speciality=doctor_data.education.speciality,
                )
                session.add(new_education)
                await session.flush()

                new_doctor = Doctors(
                    start_date=doctor_data.start_date,
                    birthday=doctor_data.birthday,
                    department_id=doctor_data.department_id,
                    user_id=new_user._id,
                    address_id=new_address._id
                )
                session.add(new_doctor)

                await session.commit()
                return new_doctor

    @classmethod
    async def delete_doctor_by_id(cls, doctor_id: int):
        async with async_session_maker() as session:
            async with session.begin():
                query = select(cls.model).filter_by(_id=doctor_id)
                result = await session.execute(query)
                doctor_to_delete = result.scalar_one_or_none()

                if not doctor_to_delete:
                    return None

                await session.execute(
                    delete(Users).filter_by(_id=doctor_to_delete.user_id)
                )

                await session.commit()
                return doctor_id

