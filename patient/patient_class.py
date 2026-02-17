from pydantic import BaseModel
from typing import Optional


class insert_patient(BaseModel):
    docter_id:str
    frist_name:str
    last_name:str
    DOB:str
    TRN: str
    Address: str

class edit_patient(BaseModel):
    patient_id:str
    docter_id:str
    frist_name:str
    last_name:str
    DOB:str
    TRN: str
    Address: str