from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from fastapi import Query


from app.services.dentist_api import DentistPlusAPI
from app.services.patient_service import PatientService
from app.services.doctor_service import DoctorService
from app.services.visit_service import VisitService

router = APIRouter()

api = DentistPlusAPI()
patient_service = PatientService(api)
doctor_service = DoctorService(api)
visit_service = VisitService(api)

class PatientCreateRequest(BaseModel):
    phone: str
    fname: str
    doctor_id: int
    lname: Optional[str] = "-"

@router.post("/find-or-create-patient")
def find_or_create_patient(request: PatientCreateRequest):
    # Сначала ищем по номеру
    patient = patient_service.find_by_phone(request.phone)
    if patient:
        return {"status": "found", "patient": patient}
    # Получаем филиал от доктора
    doctor = doctor_service.get(request.doctor_id)
    if not doctor.branches:
        raise HTTPException(status_code=400, detail="У доктора нет филиалов")
    branch_id = doctor.branches[0]["id"]
    # Создаём пациента
    patient = patient_service.create(branch_id, request.fname, request.phone, request.lname)
    return {"status": "created", "patient": patient}

class VisitCreateRequest(BaseModel):
    patient_id: int
    doctor_id: int
    start: str
    end: str
    description: Optional[str] = ""

@router.post("/create-visit")
def create_visit(request: VisitCreateRequest):
    doctor = doctor_service.get(request.doctor_id)
    if not doctor.branches:
        raise HTTPException(status_code=400, detail="У доктора нет филиалов")
    branch_id = doctor.branches[0]["id"]
    visit = visit_service.create(branch_id, request.patient_id, request.doctor_id, request.start, request.end, request.description)
    return {"status": "created", "visit": visit}


@router.get("/doctor-free-slots")
def doctor_free_slots(
    doctor_id: int = Query(..., description="ID доктора"),
    date: str = Query(..., description="Дата в формате YYYY-MM-DD"),
    slot_size: int = Query(30, description="Размер слота в минутах (по умолчанию 30)")
):
    slots = visit_service.find_free_slots(doctor_id, date, slot_size)
    return {"doctor_id": doctor_id, "date": date, "slot_size": slot_size, "free_slots": slots}