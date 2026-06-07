from modals.db_modals import Status_Table
from app_status.status_class import AppointmentStatusClassInsert, AppointmentStatusClass
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

# Get data in database base on limit
def get_all_status(db:Session,Limit:int,Offset:int):
    return db.query(Status_Table).limit(limit=Limit).offset(offset=Offset).all()

# get status by ID
def get_status_by_Id(db:Session,status_id:str):
    return db.query(Status_Table).filter( 
        Status_Table.status_id == status_id
    ).first()

# New status add to database
def create_new_status(db:Session,insert_value:AppointmentStatusClassInsert):
    try:
        new_status = Status_Table( status_name = insert_value.status_name)
        db.add(new_status)
        db.commit()

        return "New Status added."
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error adding new status"
    )

# Edit status
def edit_status(db:Session,status:AppointmentStatusClass):
    try:
        Status = get_status_by_Id(db=db,status_id=status.status_id)
        Status.status_name = status.status_name

        db.commit()
        db.refresh(Status)

        return "Status record edited."
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error editing status."
    )