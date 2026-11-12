from sqlalchemy.orm import Session
from datetime import date
from models import AppointmentModel
from schemas import AppointmentCreate, AppointmentUpdate

def check_conflict(db: Session, doctor_name: str, appt_date: date, time_slot: str, exclude_id: int = None):
    query = db.query(AppointmentModel).filter(
        AppointmentModel.doctor_name == doctor_name,
        AppointmentModel.date == appt_date,
        AppointmentModel.time_slot == time_slot,
        AppointmentModel.status != "Cancelled"
    )
    if exclude_id:
        query = query.filter(AppointmentModel.id != exclude_id)
    return query.first() is not None

def get_appointments(db: Session, doctor: str = None, status: str = None):
    query = db.query(AppointmentModel)
    if doctor:
        query = query.filter(AppointmentModel.doctor_name == doctor)
    if status:
        query = query.filter(AppointmentModel.status == status)
    return query.all()

def create_appointment(db: Session, appt: AppointmentCreate):
    db_appt = AppointmentModel(**appt.dict())
    db.add(db_appt)
    db.commit()
    db.refresh(db_appt)
    return db_appt

def update_appointment(db: Session, db_appt: AppointmentModel, appt_update: AppointmentUpdate):
    update_data = appt_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_appt, key, value)
    db.commit()
    db.refresh(db_appt)
    return db_appt

def delete_appointment(db: Session, db_appt: AppointmentModel):
    db.delete(db_appt)
    db.commit()
    return True