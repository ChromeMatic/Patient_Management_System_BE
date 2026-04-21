from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Session
from typing import Annotated
from database_config.db_config import get_db
from appointments.app_class import insert_appointment_class, edit_appointment_class
from appointments.app_services import get_all_appointments, get_appointment_by_Id, get_appointment_by_patient_id, get_todays_appointment, create_new_appointment, edit_appointment

db_dependency = Annotated[Session, Depends(get_db)]
appointment_endpoint = APIRouter(prefix="/Appointment",tags=["Appointment Endpoint"])


# This route fetch all appointments in database
@appointment_endpoint.get("/all/{limit:int}/{offset:int}",status_code=status.HTTP_200_OK)
def Fetch_all_appointments(db:db_dependency,limit:int,offset:int):
    return get_all_appointments(db=db,Limit=limit,Offset=offset)

# This route gets all appointments for today
@appointment_endpoint.get("/todays_appointments/{limit:int}/{offset:int}",status_code=status.HTTP_200_OK)
def Fetch_todays_appointments(db:db_dependency,limit:int,offset:int):
    return get_todays_appointment(db=db,Limit=limit,Offset=offset)

# This route fetch appiontment by appointment_id
@appointment_endpoint.get("/by_id/{Id:str}", status_code=status.HTTP_200_OK)
def Fetch_appointment_by_Id(db:db_dependency,Id:str):
    return get_appointment_by_Id(db=db,Id=Id)

# This route fetch all appointment by Patient Id
@appointment_endpoint.get("/by_patient_Id/{patientId:str}/{limit:int}/{offset:int}",status_code=status.HTTP_200_OK)
def Fetch_appointments_by_patient_Id(db:db_dependency,patientId:str,limit:int,offset:int):
    return get_appointment_by_patient_id(db=db,patient_id=patientId,Limit=limit,Offset=offset)

# This route create new appointment in database
@appointment_endpoint.post("/new_appointment", status_code=status.HTTP_201_CREATED)
def Created_new_appointment(db:db_dependency,value:insert_appointment_class):
    return create_new_appointment(db=db,appointment=value)

# This route edit appointment data
@appointment_endpoint.patch("/edit_appointment",status_code=status.HTTP_200_OK)
def Edit_appointment(db:db_dependency,value:edit_appointment_class):
    return edit_appointment(db=db,value=value)