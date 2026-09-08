from modals.db_modals import Appointment_Table
from appointments.app_class import insert_appointment_class, edit_appointment_class, edit_appointment_status_class
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import date, datetime

# This function gets all Appointment from Database
def get_all_appointments(db:Session,Limit:int,Offset:int):
    stmt = db.query(Appointment_Table).order_by(Appointment_Table.created_at.desc())
    appointments = stmt.limit(Limit).offset(Offset).all()
    return appointments


# This function get appointment By Id from Database
def get_appointment_by_Id(db:Session,Id:str):
    return db.query(Appointment_Table).where(
        Appointment_Table.appointment_id == Id
    ).first()

# This function gets all appiontments by patient IDs
def get_appointment_by_patient_id(db:Session,patient_id:str,Limit:int,Offset:int):
    try:
        reseult =  db.query(Appointment_Table).where(
            Appointment_Table.patient_id == patient_id
        ).order_by(Appointment_Table.created_at.desc()).limit(
            Limit
        ).offset(Offset).all()

        return reseult
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error :{err}"
        )

# This Fuction gets all Appointments base on current Today's date
def get_todays_appointment(db:Session,Limit:int,Offset:int):
    return db.query(Appointment_Table).where(
        Appointment_Table.date == date.today()
    ).limit(Limit).offset(Offset).order_by(Appointment_Table.created_at.desc()).all()

# This function edit appointment_status
def edit_appointment_status(db:Session, app_status:edit_appointment_status_class):
    try:
        appointment = get_appointment_by_Id(db=db,Id=app_status.appointment_id)
        appointment.status = app_status.status

        db.commit()
        db.refresh(appointment)

        return "status edited"
    except Exception:
              raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error in wditing appointment status."
            )

# This function creates new appointment record
def create_new_appointment(db:Session,appointment:insert_appointment_class):
    try:
        date_format = "%Y-%m-%d"

        new_appointment = Appointment_Table(
            patient_id = appointment.patient_id,
            appointment_type= appointment.appointment_type,
            status = appointment.status,
            date = datetime.strptime(appointment.date,date_format)
        )

        db.add(new_appointment)
        db.commit()

        return "New appointment added."

    except Exception as err:
          raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in creating new appointment in system: {err}"
        )
    
# This function edit appointment record
def edit_appointment(db:Session,value:edit_appointment_class):
    try:

        appointment = get_appointment_by_Id(db=db,Id=value.appointment_id)

        appointment.patient_id = value.patient_id
        appointment.appointment_type = value.appointment_type
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

