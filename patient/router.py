from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Session
from typing import Annotated
from database_config.db_config import get_db
from patient.patient_class import insert_patient,edit_patient
from patient.services import get_all_patients, get_patient_by_ID, create_new_patient, edit_patient_record

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

# This endpoint create new patient record
@patient_endpoint.post("/create-new-patient",status_code=status.HTTP_201_CREATED)
def Create_new_patient(db:db_dependency,patient:insert_patient):
    return create_new_patient(db=db,new_record=patient)