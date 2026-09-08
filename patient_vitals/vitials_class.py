from pydantic import BaseModel

class patient_vitals_insert(BaseModel):
    patient_id:str
    blood_pressure_top_value:int
    blood_pressure_bottom_value:int
    body_temperature:int
    pulse_oximetry:int
    plus_rate:int
    respiratory_rate:int
    height:int
    body_weight:int

class patient_vitals_edit(BaseModel):
    patient_vitals_id:str
    patient_id:str
    blood_pressure_top_value:int
    blood_pressure_bottom_value:int
    body_temperature:int
    pulse_oximetry:int
    plus_rate:int
    respiratory_rate:int
    height:int
    body_weight:int