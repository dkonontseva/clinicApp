from typing import Optional

from fastapi import HTTPException
from sqlalchemy import func, or_, and_, alias
from sqlalchemy.future import select
from datetime import datetime, timedelta, date

from sqlalchemy.orm import selectinload, joinedload

from app.api.talons.schema import AppointmentCreate, AppointmentResponse
from app.core.database import async_session_maker
from app.models.models import Talons, Schedules, Patients, Doctors, Departments, Users


class AppointmentsDAO:
    model = Talons

    @classmethod
    async def find_all(cls, full_name: Optional[str] = None, from_date: Optional[date] = None,
            to_date: Optional[date] = None, status: Optional[str] = None):
        async with async_session_maker() as session:
            DoctorUser = alias(Users, name="doctor_user")
            PatientUser = alias(Users, name="patient_user")

            query = (
                select(
                    Talons.date,
                    Talons.time,
                    Talons.status,
                    DoctorUser.c.last_name.label("doctor_last_name"),
                    DoctorUser.c.first_name.label("doctor_first_name"),
                    DoctorUser.c.second_name.label("doctor_second_name"),
                    PatientUser.c.last_name.label("patient_last_name"),
                    PatientUser.c.first_name.label("patient_first_name"),
                    PatientUser.c.second_name.label("patient_second_name")
                )
                .join(Doctors, Talons.doctor_id == Doctors._id)
                .join(DoctorUser, Doctors.user_id == DoctorUser.c._id)
                .join(Patients, Talons.patient_id == Patients._id)
                .join(PatientUser, Patients.user_id == PatientUser.c._id)
            )

            filter=[]

            if full_name:
                full_name_parts = full_name.split()
                search_conditions = []
                for term in full_name_parts:
                    search_conditions.append(
                        or_(
                            DoctorUser.c.first_name.ilike(f"%{term}%"),
                            DoctorUser.c.last_name.ilike(f"%{term}%"),
                            DoctorUser.c.second_name.ilike(f"%{term}%")
                        )
                    )
                filter.append(and_(*search_conditions))

            if from_date:
                filter.append(cls.model.date>=from_date)

            if to_date:
                filter.append(cls.model.date <= to_date)
            if status:
                filter.append(cls.model.status == status)

            if filter:
                query=query.where(and_(*filter))

            result = await session.execute(query)
            return [AppointmentResponse.from_row(row) for row in result.all()]

    @classmethod
    async def find_appointments(cls, patient_id: int, date: Optional[str] = date.today(), department: Optional[str] = None, full_name: Optional[str] = None):
        async with async_session_maker() as session:
            day_of_week = datetime.strptime(date, "%Y-%m-%d").strftime("%A")

            query = (
                select(
                    Doctors._id,
                    Users.last_name,
                    Users.first_name,
                    Users.second_name,
                    Users.phone_number,
                    Departments.department_name.label("department"),
                    func.coalesce(func.count(Talons._id).filter(Talons.patient_id == patient_id), 0).label(
                        "department_visits"),
                    func.coalesce(func.count(Talons._id).filter(Talons.doctor_id == Doctors._id), 0).label("doctor_visits")
                )
                .join(Departments, Doctors.department_id == Departments._id)
                .join(Schedules, Doctors._id == Schedules.doctor_id)
                .join(Users, Doctors.user_id == Users._id)
                .outerjoin(Talons, Talons.doctor_id == Doctors._id)
                .where(Schedules.day_of_week == day_of_week)
                .group_by(Doctors._id, Departments.department_name, Users.last_name, Users.first_name, Users.second_name,Users.phone_number)
            )

            # Фильтры
            if department:
                query = query.where(Departments.department_name.ilike(f"%{department}%"))

            if full_name:
                search_terms = full_name.split()
                search_conditions = []
                for term in search_terms:
                    search_conditions.append(
                        or_(
                            Users.first_name.ilike(f"%{term}%"),
                            Users.last_name.ilike(f"%{term}%"),
                            Users.second_name.ilike(f"%{term}%")
                        )
                    )
                query = query.where(and_(*search_conditions))

            # Сортировка
            query = query.order_by(
                func.count(Talons._id).filter(Talons.patient_id == patient_id).desc(),
                func.count(Talons._id).filter(Talons.doctor_id == Doctors._id).desc(),
                Users.last_name.asc()
            )

            result = await session.execute(query)
            doctors = result.all()

            return doctors

    @classmethod
    async def get_available_slots(cls, doctor_id: int, date: str):
        async with async_session_maker() as session:
            date_obj = datetime.strptime(date, "%Y-%m-%d").date()
            day_of_week = date_obj.strftime("%A")

            shift_query = await session.execute(
                select(Schedules)
                .options(selectinload(Schedules.shifts))
                .where(Schedules.doctor_id == doctor_id, Schedules.day_of_week == day_of_week)
            )
            schedule = shift_query.scalar()

            if not schedule or not schedule.shifts:
                return {"available_slots": []}

            booked_query = await session.execute(
                select(Talons.time)
                .where(Talons.doctor_id == doctor_id, Talons.date == date_obj)
            )
            booked_slots = {row[0].strftime("%H:%M") for row in booked_query.all()}

            available_slots = []
            current_time = datetime.combine(date_obj, schedule.shifts.start_time)
            end_time = datetime.combine(date_obj, schedule.shifts.end_time)

            while current_time < end_time:
                slot_time = current_time.strftime("%H:%M")
                if slot_time not in booked_slots:
                    available_slots.append(slot_time)
                current_time += timedelta(minutes=30)

            return {"available_slots": available_slots}

    @classmethod
    async def create_appointment(cls, data: AppointmentCreate, patient_id: int):
        async with async_session_maker() as session:
            async with session.begin():
                new_appointment = Talons(
                    patient_id= patient_id,
                    doctor_id = data.doctor_id,
                    date = data.date,
                    time = data.time,
                    service_id=data.service_id,
                    status = "Pending",
                )
                session.add(new_appointment)
                await session.commit()
                return new_appointment

    @classmethod
    async def delete_appointment(cls, appointment_id: int):
        async with async_session_maker() as session:
            async with session.begin():
                appointment = await session.get(Talons, appointment_id)
                if not appointment:
                    return None
                await session.delete(appointment)
                await session.commit()
                return {"message": "Appointment deleted"}

    @classmethod
    async def update_appointment(cls, appointment_id: int, data: AppointmentCreate):
        async with async_session_maker() as session:
            async with session.begin():
                query = select(cls.model).filter_by(_id=appointment_id)
                result = await session.execute(query)
                appointment = result.scalar_one_or_none()
                if not appointment:
                    return None

                for key, value in data.dict().items():
                    setattr(appointment, key, value)

                await session.commit()
                return appointment


    @classmethod
    async def get_for_doctor(cls, doctor_id: int):
        async with async_session_maker() as session:
            result = await session.execute(select(cls.model).where(cls.model.doctor_id==doctor_id, cls.model.date>=date.today()))
            return result.scalars().all()

    @classmethod
    async def get_for_patient(cls, patient_id: int):
        async with async_session_maker() as session:
            result = await session.execute(select(cls.model).where(cls.model.patient_id==patient_id, cls.model.date>=date.today()))
            return result.scalars().all()

    @classmethod
    async def get_history_for_patient(cls, patient_id: int):
        async with async_session_maker() as session:
            result = await session.execute(
                select(cls.model).where(cls.model.patient_id == patient_id, cls.model.date < date.today()))
            return result.scalars().all()
