from modals.db_modals import Docter
from docter.doctor_class import create_doctor, edit_doctor
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status

# This function gets all doctor info from database
def get_all_doctor(db:Session, limit:int, offset:int):
    return db.query(Docter).limit(limit=limit).offset(offset=offset).all()

# This function get doctor info base on docter_id
def get_doctor_by_docter_id(db:Session,docter_id:str):
    return db.query(Docter).filter(
        Docter.docter_id == docter_id
    ).first()

# This function get doctor by user_id
def get_doctor_by_user_id(db:Session,user_id:str):
    return db.query(Docter).filter(
        Docter.user_id == user_id
    ).first()

# This function create new Docter
def create_new_docter(db:Session,value:create_doctor):
    try:
        new_docter = Docter(
            user_id = value.user_id,
            frist_name = value.frist_name,
            last_name = value.last_name,
            created_at = func.now()
        )
        db.add(new_docter)
        db.commit()

        return "New Docter added."
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error in creating new Docter"
        )
    
# This function edit docter information
def edit_docter_info(db:Session,value:edit_doctor):
    try:
        docter = get_doctor_by_docter_id(db=db,docter_id=value.docter_id)

        docter.frist_name = value.frist_name
        docter.last_name = value.last_name
        docter.edited_at = func.now()

        db.commit()
        db.refresh(docter)

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error in editing Docter"
        )    