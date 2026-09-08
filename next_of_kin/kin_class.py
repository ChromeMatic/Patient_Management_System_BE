from pydantic import BaseModel

class Kin_Insert(BaseModel):
    patient_id:str
    frist_name:str
    last_name:str
    relation:str
    phone_number:str
    current_address:str

class Edit_Kin(BaseModel):
    next_of_kin_id:str
    patient_id:str
    frist_name:str
    last_name:str
    relation:str
    phone_number:str
    current_address:str