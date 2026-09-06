from pydantic import BaseModel

class AppointmentStatusClass(BaseModel):
    status_id:str
    status_name:str

class AppointmentStatusClassInsert(BaseModel):
    status_name:str