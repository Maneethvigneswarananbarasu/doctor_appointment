from datetime import date
from pydantic import BaseModel
from typing import Optional

class AppointmentCreate(BaseModel):
    patient_name: str
    doctor_name: str
    date: date
    time_slot: str
    status: Optional[str] = "Booked"

class AppointmentUpdate(BaseModel):
    patient_name: Optional[str] = None
    doctor_name: Optional[str] = None
    date: Optional[date] = None
    time_slot: Optional[str] = None
    status: Optional[str] = None

class AppointmentResponse(AppointmentCreate):
    id: int

    class Config:
        orm_mode = True