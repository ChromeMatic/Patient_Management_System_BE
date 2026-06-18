from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Session
from typing import Annotated
from database_config.db_config import get_db
from patient.patient_class import insert_patient,edit_patient, next_of_kin, Patient_Search
from patient.services import get_all_patients, get_patient_by_ID, create_new_patient, edit_patient_record, get_all_next_of_kin_record, search_by

patient_endpoint = APIRouter( prefix="/Patient",tags=["Patient Endpoints"])
db_dependency = Annotated[Session, Depends(get_db)]

# This endpoint gets all patients information
@patient_endpoint.get("/all/{limit:int}/{offset:int}",status_code=status.HTTP_200_OK)
def Fetch_all_patients(db:db_dependency,limit:int,offset:int):
    return get_all_patients(db=db,limnit=limit,offset=offset)

# This endpoint gets patient by ID
@patient_endpoint.get("/by-Id/{ID:str}",status_code=status.HTTP_200_OK)
def Fetch_patient_by_id(db:db_dependency,ID:str):
    return get_patient_by_ID(db=db,Id=ID)

# This endpoint fetch all next of kin record
@patient_endpoint.get("/all-next-of-kin/{limit:int}/{offset:int}")
def Fetch_all_next_of_kin_record(db:db_dependency,limit:int,offset:int):
    return get_all_next_of_kin_record(db=db,limnit=limit,offset=offset)

# This endpoint handles patient search
@patient_endpoint.post("/search", status_code=status.HTTP_200_OK)
def Search_Patient(db:db_dependency,Value:Patient_Search):
    return search_by(db=db,value=Value)

# This endpoint create new patient record
@patient_endpoint.post("/create-new-patient",status_code=status.HTTP_201_CREATED)
def Create_new_patient(db:db_dependency,patient:insert_patient,kin:next_of_kin):
    return create_new_patient(db=db,new_record=patient,new_kin=kin)

# This endpoint edit patient record
@patient_endpoint.patch("/edit-patient",status_code=status.HTTP_200_OK)
def Edit_patient_record(db:db_dependency,patient:edit_patient):
    return edit_patient_record(db=db,record=patient)