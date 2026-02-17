from modals.db_modals import Patient
from  patient.patient_class import insert_patient,edit_patient
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

# This function gets all patients from Database
def get_all_patients(db:Session,limnit:int,offset:int):
    return db.query(Patient).limit(limit=limnit).offset(offset=offset).all()

# This function get patient by ID
def get_patient_by_ID(db:Session,Id:str):
    return db.query(Patient).filter(Patient.patient_id == Id).first()

# This function gets all Patient by docter ID    
def get_patients_by_docter(db:Session,doctor_id:str,limnit:int,offset:int):
    try:
        result = db.query(Patient).filter(
            Patient.docter_id ==  doctor_id
        ).limit(limit=limnit).offset(offset=offset).all()

        return result
    except Exception:
          raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error in Fetching patient database."
        )
    
# This function creates a new patient
def create_new_patient(db:Session,new_record:insert_patient):
    try:
        new_patient = Patient(
            docter_id = new_record.docter_id,
            frist_name = new_record.frist_name,
            last_name = new_record.last_name,
            DOB = new_record.DOB,
            TRN = new_record.TRN,
            Address =  new_record.Address
        )

        db.add(new_patient)
        db.commit()

        return "New Patient added."
    except Exception:
          db.rollback()
          raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error in create new patient in database."
        )
    
# This funtion edit patient record
def edit_patient_record(db:Session,record:edit_patient):
    try:
        patient_record = get_patient_by_ID(db=db,Id=record.patient_id)

        patient_record.docter_id = record.docter_id
        patient_record.frist_name = record.frist_name
        patient_record.last_name = record.last_name
        patient_record.DOB = record.DOB
        patient_record.TRN = record.TRN
        patient_record.Address = record.Address
        patient_record.edited_at =  func.now()

        db.commit()
        db.refresh(patient_record)

        return "Patient record has been edited."
    except Exception:
          db.rollback()
          raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error in editing patient record."
        )    
    