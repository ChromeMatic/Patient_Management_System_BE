from modals.db_modals import Next_Of_Kin
from next_of_kin.kin_class import Edit_Kin, Kin_Insert
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


# Fetch all Next of Kin all records
def get_all_next_of_kin_records(db:Session,limnit:int,offset:int):
    query = db.query(Next_Of_Kin).order_by(Next_Of_Kin.created_at.desc())
    _data = query.limit(limit=limnit).offset(offset=offset).all()
    return _data

# Fetch Next of Kin all record by Id 
def get_record_by_id(db:Session,Id:str):
    return db.query(Next_Of_Kin).filter(
        Next_Of_Kin.next_of_kin_id == Id
    ).first()

# Fetch Next of Kin all record by patient_id 
def get_records_by_patient_id(db:Session,Id:str):
    return db.query(Next_Of_Kin).filter(
        Next_Of_Kin.patient_id == Id
    ).all()

# Create new Next of Kin record
def create_new_record(db:Session,value:Kin_Insert):
    try:
        new_rec = Next_Of_Kin(
            patient_id = value.patient_id,
            frist_name = value.frist_name,
            last_name = value.last_name,
            relation = value.relation,
            phone_number = value.phone_number,
            current_address = value.current_address
        )

        db.add(new_rec)
        db.commit()

        return "New Next of Kin record added."

    except Exception as err:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in create new Next of Kin record in database: {err}"
        )
    
# Edit Next Of Kin record
def edit_record(db:Session,value:Edit_Kin):
    try:

        rec = get_record_by_id(db=db,Id=value.next_of_kin_id)

        rec.patient_id = value.patient_id
        rec.frist_name = value.frist_name
        rec.last_name = value.last_name
        rec.relation = value.relation,
        rec.phone_number = value.phone_number,
        rec.current_address = value.current_address
        rec.edited_at = func.now()

        db.commit()
        db.refresh(rec)

        return "Next Of Kin record edited"

    except Exception as err:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in create new Next of Kin record in database: {err}"
        )