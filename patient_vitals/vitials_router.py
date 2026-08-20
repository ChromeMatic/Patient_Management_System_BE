from fastapi import Depends, APIRouter, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Annotated
from database_config.db_config import get_db
from patient_vitals.vitials_class import patient_vitals_insert, patient_vitals_edit
from patient_vitals.vitials_services import get_vital_by_id, get_vital_by_patient_Id, create_new_record, edit_patient_info
from user_authenication.auth_service import verify_jwt_access_token

vital_endpoint = APIRouter( prefix="/Vitals",tags=["Patient Vitals Endpoint"])
db_dependency = Annotated[Session, Depends(get_db)]
oauth2_bear = OAuth2PasswordBearer(tokenUrl='auth/token')

# This endpoint gets vital data by Id
@vital_endpoint.get("/by_vital_id/{Id:str}",status_code=status.HTTP_200_OK)
def Fetch_vitals_by_Id(db:db_dependency,Id:str,token:Annotated[str,Depends(oauth2_bear)]):
    user_info = verify_jwt_access_token(jwt_token=token,db=db)

    if user_info not in ['supervisor','admin','doctor','nurse']:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is unauthorized to view data"
        )
    else:
        return get_vital_by_id(db=db,vital_id=Id)

# This endpoint gets vital data by patient Id
@vital_endpoint.get("/by_patient_id/{patient_id}",status_code=status.HTTP_200_OK)
def Fetch_vitals_by_by_patient_id(db:db_dependency,patient_id:str,token:Annotated[str,Depends(oauth2_bear)]):
    user_info = verify_jwt_access_token(jwt_token=token,db=db)

    if user_info not in ['supervisor','admin','doctor','nurse']:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is unauthorized to view data"
        )
    else:
        return get_vital_by_patient_Id(db=db,patient_id=patient_id)

# This endpoint create new vital record in database
@vital_endpoint.post("/create",status_code=status.HTTP_201_CREATED)
def Create_new_recrd(db:db_dependency,record:patient_vitals_insert,token:Annotated[str,Depends(oauth2_bear)]):
    user_info = verify_jwt_access_token(jwt_token=token,db=db)

    if user_info not in ['supervisor','admin','doctor','nurse']:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is unauthorized to view data"
        )
    else:
        return create_new_record(db=db,new_record=record)

# This endpoint edit vital data
@vital_endpoint.patch("/edit_vital_info",status_code=status.HTTP_200_OK)
def Edit_vital_data(db:db_dependency,vital_data:patient_vitals_edit,token:Annotated[str,Depends(oauth2_bear)]):
    user_info = verify_jwt_access_token(jwt_token=token,db=db)

    if user_info not in ['supervisor','admin','doctor','nurse']:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is unauthorized to view data"
        )
    else:
        return edit_patient_info(db=db,value=vital_data)