from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Session
from typing import Annotated
from database_config.db_config import get_db
from app_status.status_class import AppointmentStatusClassInsert, AppointmentStatusClass
from app_status.status_services import get_all_status,get_status_by_Id, create_new_status, edit_status

status_endpoint = APIRouter( prefix="/Status",tags=["Status Endpoint"])
db_dependency = Annotated[Session, Depends(get_db)]

# Fetch all status
@status_endpoint.get("/all_status/{Limit:int}/{Offset:int}",status_code=status.HTTP_200_OK)
def fetch_all_status(db:db_dependency,Limit:int,Offset:int):
    return get_all_status(db=db,Limit=Limit,Offset=Offset)

# Fetch status by Id
@status_endpoint.get("/by-Id/{statusId:str}",status_code=status.HTTP_200_OK)
def fetch_status_by_Id(db:db_dependency,status_id:str):
    return get_status_by_Id(db=db,status_id=status_id)

# Create new status in DB
@status_endpoint.post("/create",status_code=status.HTTP_201_CREATED)
def Create_new_status(db:db_dependency,new_status:AppointmentStatusClassInsert):
    return create_new_status(db=db,insert_value=new_status)

# Edit status
@status_endpoint.patch("/edit",status_code=status.HTTP_200_OK)
def Edit_status(db:db_dependency,status:AppointmentStatusClass):
    return edit_status(db=db,status=status)