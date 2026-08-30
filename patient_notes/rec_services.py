from modals.db_modals import Patients_Records
from patient_notes.rec_class import patient_note_edit, patient_note_insert
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

# Get patient notes by Id
def get_patient_note_by_Id(db:Session,Id:str):
    return db.query(Patients_Records).filter(
        Patients_Records.record_id == Id
    ).order_by(Patients_Records.created_at.desc()).first()

# Get patient notes by patient ID
def get_patient_notes_by_patientID(db:Session,patient_id:str,limit:int,offset:int):
    query = db.query(Patients_Records).filter( 
        Patients_Records.patient_id == patient_id
    ).order_by(Patients_Records.created_at.desc())
    notes = query.limit(limit=limit).offset(offset=offset).all()
    return notes

# Create new patient notes record
def create_new_notes_record(db:Session,record:patient_note_insert):
    try:

        New_Notes = Patients_Records(
            patient_id = record.patient_id,
            presenting_complain = record.presenting_complain,
            patient_diagnosis = record.patient_diagnosis,
            patient_treatment = record.patient_treatment,
            notes = record.notes
        )

        db.add(New_Notes)
        db.commit()

        return "New patient note added."
    
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in creating patient notes"
        )

# Edit patient notes recordd
def edit_patient_note_record(db:Session,record:patient_note_edit):
    try:

        edit_record = get_patient_note_by_Id(db=db,Id=record.record_id)

        edit_record.patient_id = record.patient_id
        edit_record.presenting_complain = record.presenting_complain
        edit_record.patient_diagnosis = record.patient_diagnosis
        edit_record.patient_treatment = record.patient_treatment
        edit_record.notes = record.notes

        db.commit()
        db.refresh(edit_record)

        return "Paatient note record added."
    
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error in editing patient note record."
        )