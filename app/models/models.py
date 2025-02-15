from datetime import datetime

from sqlalchemy import Column, Integer, Time, DateTime, String, ForeignKey, SmallInteger, Float, Date
from sqlalchemy.orm import declarative_base, relationship

from app.core.database import engine, Base


class Roles(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    role = Column(String, nullable=False)
    users = relationship('Users', backref='roles')

class Users(Base):
    __tablename__ = 'users'

    _id = Column(Integer, primary_key=True)
    login = Column(String, unique=True)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    second_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'))
    patients = relationship('Patients', backref='users', uselist=False)
    doctors = relationship('Doctors', backref='users', uselist=False)
    roles = relationship('Roles', backref='users')
    chat_messages = relationship('ChatMessages', backref='users')

class Patients(Base):
    __tablename__ = 'patients'

    _id = Column(Integer, primary_key=True, autoincrement=True)
    b_date = Column(Date, nullable=False)
    user_id = Column(Integer, ForeignKey('users._id'))
    address_id = Column(Integer, ForeignKey('addresses._id'))
    medical_cards = relationship('MedicalCards', backref='patients')
    talons = relationship('Talons', backref='patients')

class Doctors(Base):
    __tablename__ = 'doctors'

    _id = Column(Integer, primary_key=True, autoincrement=True)
    start_date=Column(Date, nullable=False)
    birthday=Column(Date, nullable=False)
    user_id = Column(Integer, ForeignKey('users._id'))
    address_id = Column(Integer, ForeignKey('addresses._id'))
    department_id = Column(Integer, ForeignKey('departments._id'))
    doctor_leaves = relationship('DoctorLeaves', backref='doctors')
    medical_cards = relationship('MedicalCards', backref='doctors')
    talons = relationship('Talons', backref='doctors')
    schedules = relationship('Schedule', backref='doctors')

class Addresses(Base):
    __tablename__ = 'addresses'

    _id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String, nullable=False)
    city = Column(String, nullable=False)
    street = Column(String, nullable=False)
    house_number = Column(String, nullable=False)
    flat_number = Column(String, nullable=False)
    doctors = relationship('Doctors', backref='addresses')
    patients = relationship('Patients', backref='addresses')
    educations = relationship('Education', backref='addresses')

class Departments(Base):
    __tablename__ = 'departments'

    _id = Column(Integer, primary_key=True, autoincrement=True)
    department_name = Column(String, nullable=False)
    doctors = relationship('Doctors', backref='departments')


class Services(Base):
    __tablename__ = 'services'

    _id = Column(Integer, primary_key=True, autoincrement=True)
    service = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    talons = relationship('Talons', backref='services')


class DoctorLeaves(Base):
    __tablename__ = 'doctor_leaves'

    _id = Column(Integer, primary_key=True, autoincrement=True)
    from_date = Column(Date, nullable=False)
    to_date = Column(Date, nullable=False)
    leave_type = Column(String, nullable=False)
    reason = Column(String, nullable=False)
    status = Column(String, nullable=False)
    doctors = relationship('Doctors', backref='doctor_leaves')


class Education(Base):
    __tablename__ = 'education'

    _id = Column(Integer, primary_key=True, autoincrement=True)
    university = Column(String, nullable=False)
    faculty = Column(String, nullable=False)
    speciality = Column(String, nullable=False)
    doctors = relationship('Doctors', backref='education')


class MedicalCards(Base):
    __tablename__ = 'medical_cards'

    _id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    complaints = Column(String, nullable=False)
    wellness_check = Column(String, nullable=False)
    diagnosis = Column(String, nullable=False)
    doctor_id = Column(Integer, ForeignKey('doctors._id'))
    patient_id = Column(Integer, ForeignKey('patients._id'))


class Schedules(Base):
    __tablename__ = 'schedules'

    _id = Column(Integer, primary_key=True, autoincrement=True)
    day_of_week = Column(String, nullable=False)
    doctor_id = Column(Integer, ForeignKey('doctors._id'))
    shift_id = Column(Integer, ForeignKey('shifts._id'))


class Shifts(Base):
    __tablename__ = 'shifts'

    _id = Column(Integer, primary_key=True, autoincrement=True)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    schedules = relationship('Schedules', backref='shifts')


class Talons(Base):
    __tablename__ = 'talons'

    _id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    status = Column(String, nullable=False)
    purpose = Column(String)
    patient_id = Column(Integer, ForeignKey('patients._id'))
    doctor_id = Column(Integer, ForeignKey('doctors._id'))
    service_id = Column(Integer, ForeignKey('services._id'))


class ChatMessages(Base):
    __tablename__ = 'chat_messages'

    _id = Column(Integer, primary_key=True, autoincrement=True)
    message = Column(String, nullable=False)
    timestapm = Column(DateTime, default=datetime.now)
    user_id = Column(Integer, ForeignKey('users._id'))


