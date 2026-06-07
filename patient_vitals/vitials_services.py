from modals.db_modals import Patient_Blood_Pressure_Vitals
from patient_vitals.vitials_class import patient_vitals_insert,patient_vitals_edit
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

# Fetch all vitals
def get_vital_by_id(db:Session,vital_id:str):
    return db.query(Patient_Blood_Pressure_Vitals).filter(
        Patient_Blood_Pressure_Vitals.patient_vitals_id == vital_id
    ).order_by().first()

# Fetch all vitals by patient id
def get_vital_by_patient_Id(db:Session,patient_id:str):
    return db.query(Patient_Blood_Pressure_Vitals).filter(
        Patient_Blood_Pressure_Vitals.patient_id == patient_id
    ).all()

# Create New Vital data in database
def create_new_record(db:Session,new_record:patient_vitals_insert):
    try:
        record = Patient_Blood_Pressure_Vitals(
            patient_id = new_record.patient_id,
            blood_pressure_top_value = new_record.blood_pressure_top_value,
            blood_pressure_bottom_value = new_record.blood_pressure_bottom_value,
            body_temperature = new_record.body_temperature,
            pulse_oximetry = new_record.pulse_oximetry,
            plus_rate = new_record.plus_rate,
            respiratory_rate = new_record.respiratory_rate,
            height = new_record.height,
            body_weight =  new_record.body_weight
        )

        db.add(record)
        db.commit()

        return "New vitals added."
    
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in create new vital record in database."
        )
    
# Edit Vital data
def edit_patient_info(db:Session,value:patient_vitals_edit):
    try:

        info = get_vital_by_id(db=db,vital_id=value.patient_id)

        info.patient_id = value.patient_id
        info.blood_pressure_top_value= value.blood_pressure_top_value
        info.blood_pressure_bottom_value= value.blood_pressure_bottom_value
        info.body_temperature = value.body_temperature,
        info.pulse_oximetry = value.pulse_oximetry,
        info.plus_rate = value.plus_rate,
        info.respiratory_rate = value.respiratory_rate,
        info.height = value.height,
        info.body_weight =  value.body_weight

        db.commit()
        db.refresh(info)

        return "Patient vitals edited"

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in editing patient vitals record in database."
        )   