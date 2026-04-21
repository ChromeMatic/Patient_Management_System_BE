from modals.db_modals import Appointment_Table
from appointments.app_class import insert_appointment_class, edit_appointment_class
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import date

# This function gets all Appointment from Database
def get_all_appointments(db:Session,Limit:int,Offset:int):
    return db.query(Appointment_Table).limit(Limit).offset(Offset).all()


# This function get appointment By Id from Database
def get_appointment_by_Id(db:Session,Id:str):
    return db.query(Appointment_Table).where(
        Appointment_Table.appointment_id == Id
    ).first()

# This function gets all appiontments by patient IDs
def get_appointment_by_patient_id(db:Session,patient_id:str,Limit:int,Offset:int):
    return db.query(Appointment_Table).where(
        Appointment_Table.patient_id == patient_id
    ).limit(Limit).offset(Offset).all()

# This Fuction gets all Appointments base on current Today's date
def get_todays_appointment(db:Session,Limit:int,Offset:int):
    return db.query(Appointment_Table).where(
        Appointment_Table.date == date.today()
    ).limit(Limit).offset(Offset).all()

# This function creates new appointment record
def create_new_appointment(db:Session,appointment:insert_appointment_class):
    try:

        new_appointment = Appointment_Table(
            patient_id = appointment.patient_id,
            status = appointment.status,
            date = appointment.date
        )

        db.add(new_appointment)
        db.commit()

        return "New appointment added."

    except Exception:
          raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error in creating new appointment in system."
        )
    
# This function edit appointment record
def edit_appointment(db:Session,value:edit_appointment_class):
    try:

        appointment = get_appointment_by_Id(db=db,Id=value.appointment_id)

        appointment.patient_id = value.patient_id
        appointment.status = value.status
        appointment.date = value.date

        db.commit()
        db.refresh(appointment)

        return "Appointment infomation updated."
    except Exception:
        raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Error in editing appointment record."
    )


# Queue implemetation