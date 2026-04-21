from pydantic import BaseModel
from typing import Optional


class insert_patient(BaseModel):
    frist_name:str
    last_name:str
    DOB:str
    TRN: str
    phone_number: str
    Address: str

class edit_patient(BaseModel):
    patient_id:str
    docter_id:str
    frist_name:str
    last_name:str
    DOB:str
    TRN: str
    Address: str

class Insert_Next_Of_Kin(BaseModel):
    next_of_kin_id:Optional[str]
    patient_id:Optional[str]
    frist_name:str
    last_name:str
    relation:str
    phone_number:str
    current_address:str

class Edit_Next_Of_Kin(BaseModel):
    next_of_kin_id:str
    patient_id:str
    frist_name:str
    last_name:str
    relation:str
    phone_number:str
    current_address:str