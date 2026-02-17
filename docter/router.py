from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Session
from typing import Annotated
from database_config.db_config import get_db
from docter.doctor_class import create_doctor, edit_doctor
from docter.services import get_all_doctor,get_doctor_by_docter_id,get_doctor_by_user_id,create_new_docter,edit_docter_info

docter_endpoint = APIRouter( prefix="/Doctor",tags=["Dotor Endpoint"])
db_dependency = Annotated[Session, Depends(get_db)]

# This endpoint gets all doctor information
@docter_endpoint.get("/{limit:int}/{offset:int}",status_code=status.HTTP_200_OK)
def Fetch_all_docter_info(db:db_dependency,limit:int,offset:int):
    return get_all_doctor(db=db,limit=limit,offset=offset)

# This endpoint gets doctor by docter_id
@docter_endpoint.get("/{doctor_id:str}",status_code=status.HTTP_200_OK)
def Fetch_doctor_by_Id(db:db_dependency,doctor_id:str):
    return get_doctor_by_docter_id(db=db,docter_id=doctor_id)

# This endpoint get doctor by user_id
@docter_endpoint.get("/by_user_id/{user_id:str}", status_code=status.HTTP_200_OK)
def Fetch_doctor_by_Id(db:db_dependency,user_id:str):
    return get_doctor_by_user_id(db=db,user_id=user_id)

# This endpoint create new doctor record in databse
@docter_endpoint.post("/create", status_code=status.HTTP_201_CREATED)
def Create_new_doctor_record(db:db_dependency,new_value:create_doctor):
    return create_new_docter(db=db,value=new_value)

#  This endpoint edit docter information
@docter_endpoint.patch("/edit", status_code=status.HTTP_200_OK)
def Edit_doctor_info(db:db_dependency,values:edit_doctor):
    return edit_docter_info(db=db,value=values)