from pydantic import BaseModel

class patient_vitals_insert(BaseModel):
    patient_id:str
    blood_pressure_top_value:str
    blood_pressure_bottom_value:str
    body_temperature:str
    pulse_oximetry:str
    plus_rate:str
    respiratory_rate:str
    height:str
    body_weight:str

class patient_vitals_edit(BaseModel):
    patient_vitals_id:str
    patient_id:str
    blood_pressure_top_value:str
    blood_pressure_bottom_value:str
    body_temperature:str
    pulse_oximetry:str
    plus_rate:str
    respiratory_rate:str
    height:str
    body_weight:str