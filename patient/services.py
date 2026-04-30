from modals.db_modals import Patient, Next_Of_Kin, Patients_Records
from patient.patient_class import insert_patient,edit_patient, next_of_kin, Edit_Next_Of_Kin
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status

# This function gets all patients from Database
def get_all_patients(db:Session,limnit:int,offset:int):
    return db.query(Patient).limit(limit=limnit).offset(offset=offset).all()

# This function get patient by ID
def get_patient_by_ID(db:Session,Id:str):
    return (
        db.query(Patient)
        .options(
            joinedload(Patient.relative),
            joinedload(Patient.history)
        )
        .filter(Patient.patient_id == Id)
        .first()
    )

# This function gets all next of kin records
def get_all_next_of_kin_record(db:Session,limnit:int,offset:int):
    return db.query(Next_Of_Kin).limit(limit=limnit).offset(offset=offset).all()

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
def create_new_patient(db:Session,new_record:insert_patient,new_kin:next_of_kin):
    try:
        new_patient = Patient(
            frist_name = new_record.frist_name,
            last_name = new_record.last_name,
            DOB = new_record.DOB,
            TRN = new_record.TRN,
            Address =  new_record.Address,
            phone_number = new_record.phone_number
        )

        db.add(new_patient)
        db.flush()

        record = Next_Of_Kin(
           patient_id = new_patient.patient_id,
           frist_name = new_kin.frist_name,
           last_name = new_kin.last_name,
           relation = new_kin.relation,
           phone_number = new_kin.phone_number,
           current_address = new_kin.current_address
        )
        
        db.add(record)
        
        db.commit()
        db.refresh(new_patient)

        return "New Patient and Next of Kin record added."
    except Exception as err:
          db.rollback()
          raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in create new patient in database: {err}"
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
    