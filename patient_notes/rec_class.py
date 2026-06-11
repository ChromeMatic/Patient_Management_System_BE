from pydantic import BaseModel


class patient_note_insert(BaseModel):
    patient_id:str
    presenting_complain:str
    patient_diagnosis:str
    patient_treatment:str
    notes:str

class patient_note_edit(BaseModel):
    record_id:str
    patient_id:str
    patient_vitals:str
    presenting_complain:str
    patient_diagnosis:str
    patient_treatment:str
    notes:str