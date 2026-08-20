from fastapi import Depends, APIRouter, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Annotated
from database_config.db_config import get_db
from next_of_kin.kin_class import Edit_Kin, Kin_Insert
from next_of_kin.kin_services import get_all_next_of_kin_records,get_record_by_id,get_records_by_patient_id,create_new_record,edit_record
from user_authenication.auth_service import verify_jwt_access_token

kin_endpoint = APIRouter( prefix="/Next_Of_Kin",tags=["Next Of Kin Endpoint"])
db_dependency = Annotated[Session, Depends(get_db)]
oauth2_bear = OAuth2PasswordBearer(tokenUrl='auth/token')

# This route gets all Next of Kin records from database
@kin_endpoint.get("/all/{limit:int}/{offset:int}",status_code=status.HTTP_200_OK)
def Fetch_all_records(db:db_dependency,limit:int,offset:int,token:Annotated[str,Depends(oauth2_bear)]):
    user_info = verify_jwt_access_token(jwt_token=token,db=db)
    
    if user_info not in ['supervisor','admin','doctor','nurse']:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is unauthorized to view data"
        )
    else:
        return  get_all_next_of_kin_records(db=db,limnit=limit,offset=offset) 

# This route gets all Next of Kin record by Id
@kin_endpoint.get("/By_Id/{kin_id}",status_code=status.HTTP_200_OK)
def Fetch_by_Id(db:db_dependency,kin_id:str,token:Annotated[str,Depends(oauth2_bear)]):
    user_info = verify_jwt_access_token(jwt_token=token,db=db) 

    if user_info not in ['supervisor','admin','doctor','nurse']:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is unauthorized to view data"
        )
    else:
        return get_record_by_id(db=db,Id=kin_id)

# This route gets all record by Patient Id
@kin_endpoint.get("/by_patient_id/{patient_id}",status_code=status.HTTP_200_OK)
def Fetch_by_patient_id(db:db_dependency,patient_id:str,token:Annotated[str,Depends(oauth2_bear)]):
    user_info = verify_jwt_access_token(jwt_token=token,db=db)
   
    if user_info not in ['supervisor','admin','doctor','nurse']:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is unauthorized to view data"
        )
    else:
        return  get_records_by_patient_id(db=db,Id=patient_id)

# Add new record to database
@kin_endpoint.post("/add",status_code=status.HTTP_201_CREATED)
def Create_new_record(db:db_dependency,record:Kin_Insert,token:Annotated[str,Depends(oauth2_bear)]):
    user_info = verify_jwt_access_token(jwt_token=token,db=db)
   
    if user_info not in ['supervisor','admin','doctor','nurse']:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is unauthorized to view data"
        )
    else:
        return create_new_record(db=db,value=record)

# Edit record in database
@kin_endpoint.patch("/edit",status_code=status.HTTP_200_OK)
def Edit_record(db:db_dependency,value:Edit_Kin,token:Annotated[str,Depends(oauth2_bear)]):
    user_info = verify_jwt_access_token(jwt_token=token,db=db)
   
    if user_info not in ['supervisor','admin','doctor','nurse']:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is unauthorized to view data"
        )
    else:
        return edit_record(db=db,value=value)