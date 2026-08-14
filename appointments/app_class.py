from pydantic import BaseModel
from typing import Optional


class insert_appointment_class(BaseModel):
    patient_id: str
    appointment_type: str
    status: str
    date: str


class edit_appointment_class(BaseModel):
    appointment_id: str
    patient_id: str
    appointment_type: str
    status: str
    date: str


class edit_appointment_status_class(BaseModel):
    appointment_id: str
    patient_id: str
    status: str