from fastapi import APIRouter, Depends, HTTPException, status

from app.api.address.dao import AddressDAO
from app.api.auth.dao import UsersDAO
from app.api.patients.dao import PatientsDAO
from app.api.patients.schemas import PatientResponseSchema, PatientCreateSchema, PatientUpdateSchema

router = APIRouter(prefix='/patients', tags=['Patient'])

@router.get("/", summary="Получить всех пациентов", response_model=list[PatientResponseSchema])
async def get_all_patients():
    patients= await PatientsDAO.get_full_data()
    return patients

@router.get('/{id}', summary="Получить пациента по id", response_model=PatientResponseSchema)
async def get_patient(id: int):
    patient = await PatientsDAO.get_by_id(int(id))
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "Пользователь не найден"
        )
    return patient

@router.post('/add_patient', summary='Добавить пациента')
async def add_patient(patient_data: PatientCreateSchema) -> dict:
    existing_user = await UsersDAO.find_one_or_none(login=patient_data.users.login)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь уже существует"
        )

    await PatientsDAO.add_patient(patient_data)
    return {"message": "Пациент успешно добавлен!"}

@router.delete("/delete/{patient_id}")
async def dell_student_by_id(patient_id: int) -> dict:
    check = await PatientsDAO.delete_patient_by_id(patient_id=patient_id)
    if check:
        return {"message": f"Пациент с ID {patient_id} удален!"}
    else:
        return {"message": "Ошибка при удалении Пациента!"}

@router.put("/update/{patient_id}")
async def update_patients(patient_id: int, request: PatientUpdateSchema) -> dict:

    user_id, address_id = await PatientsDAO.update_patient(patient_id, request)
    if request.users and user_id:
        await UsersDAO.update(user_id, request.users.model_dump(exclude_unset=True))

    if request.addresses and address_id:
        await AddressDAO.update(address_id, request.addresses.model_dump(exclude_unset=True))

    return {"message": "Данные пациента успешно обновлены"}
