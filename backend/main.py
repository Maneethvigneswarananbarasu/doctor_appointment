from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional

from database import engine, Base, get_db
from models import AppointmentModel
from schemas import AppointmentCreate, AppointmentUpdate, AppointmentResponse
import crud

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Doctor Appointment Booking API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/appointments", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
def create_appointment(appt: AppointmentCreate, db: Session = Depends(get_db)):
    if appt.status != "Cancelled" and crud.check_conflict(db, appt.doctor_name, appt.date, appt.time_slot):
        raise HTTPException(
            status_code=409,
            detail=f"Rejected: {appt.doctor_name} is already booked at {appt.time_slot} on {appt.date}"
        )
    return crud.create_appointment(db=db, appt=appt)

@app.get("/appointments", response_model=list[AppointmentResponse])
def list_appointments(
    doctor: Optional[str] = None, 
    status: Optional[str] = None, 
    db: Session = Depends(get_db)
):
    return crud.get_appointments(db=db, doctor=doctor, status=status)

@app.put("/appointments/{appointment_id}", response_model=AppointmentResponse)
def update_appointment(
    appointment_id: int, 
    appt_update: AppointmentUpdate, 
    db: Session = Depends(get_db)
):
    db_appt = db.query(AppointmentModel).filter(AppointmentModel.id == appointment_id).first()
    if not db_appt:
        raise HTTPException(status_code=404, detail="Appointment not found")

    target_doctor = appt_update.doctor_name if appt_update.doctor_name is not None else db_appt.doctor_name
    target_date = appt_update.date if appt_update.date is not None else db_appt.date
    target_slot = appt_update.time_slot if appt_update.time_slot is not None else db_appt.time_slot
    target_status = appt_update.status if appt_update.status is not None else db_appt.status

    if target_status != "Cancelled":
        if crud.check_conflict(db, target_doctor, target_date, target_slot, exclude_id=appointment_id):
            raise HTTPException(
                status_code=409,
                detail=f"Rejected: {target_doctor} is already booked at {target_slot} on {target_date}"
            )

    return crud.update_appointment(db=db, db_appt=db_appt, appt_update=appt_update)

@app.delete("/appointments/{appointment_id}")
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    db_appt = db.query(AppointmentModel).filter(AppointmentModel.id == appointment_id).first()
    if not db_appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    crud.delete_appointment(db=db, db_appt=db_appt)
    return {"message": "Appointment deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)