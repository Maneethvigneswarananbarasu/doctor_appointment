from sqlalchemy import Column, Integer, String, Date
from database import Base

class AppointmentModel(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String, nullable=False)
    doctor_name = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    time_slot = Column(String, nullable=False)
    status = Column(String, default="Booked")