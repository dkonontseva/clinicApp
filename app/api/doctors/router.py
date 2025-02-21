from fastapi import APIRouter, Depends, HTTPException, status

from app.api.address.dao import AddressDAO
from app.api.auth.dao import UsersDAO
from app.api.doctors.dao import DoctorsDAO
from app.api.doctors.schemas import DoctorResponseSchema, DoctorUpdateSchema

router = APIRouter(prefix='/doctors', tags=['doctor'])

@router.get("/", summary="Получить всех врачей", response_model=list[DoctorResponseSchema])
async def get_all_doctors():
    doctors= await DoctorsDAO.get_full_data()
    return doctors

@router.get('/{id}', summary="Получить врача по id", response_model=DoctorResponseSchema)
async def get_doctor(id: int):
    doctor = await DoctorsDAO.get_by_id(int(id))
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "Пользователь не найден"
        )
    return doctor

@router.post('/add_doctor', summary='Добавить врача')
async def add_doctor(doctor_data: DoctorUpdateSchema) -> dict:
    existing_user = await UsersDAO.find_one_or_none(login=doctor_data.users.login)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь уже существует"
        )

    await DoctorsDAO.add_doctor(doctor_data)
    return {"message": "Врач успешно добавлен!"}
#
# @router.delete("/delete/{doctor_id}")
# async def dell_student_by_id(doctor_id: int) -> dict:
#     check = await DoctorsDAO.delete_doctor_by_id(doctor_id=doctor_id)
#     if check:
#         return {"message": f"Врач с ID {doctor_id} удален!"}
#     else:
#         return {"message": "Ошибка при удалении Врача!"}
#
# @router.put("/update/{doctor_id}")
# async def update_doctors(doctor_id: int, request: doctorUpdateSchema) -> dict:
#
#     user_id, address_id = await DoctorsDAO.update_doctor(doctor_id, request)
#     if request.users and user_id:
#         await UsersDAO.update(user_id, request.users.model_dump(exclude_unset=True))
#
#     if request.addresses and address_id:
#         await AddressDAO.update(address_id, request.addresses.model_dump(exclude_unset=True))
#
#     return {"message": "Данные врача успешно обновлены"}
