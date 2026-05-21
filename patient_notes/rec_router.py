from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Session
from typing import Annotated
from database_config.db_config import get_db
from patient_notes.rec_class import patient_note_insert, patient_note_edit
from patient_notes.rec_services import get_patient_note_by_Id, get_patient_notes_by_patientID, create_new_notes_record, edit_patient_note_record

notes_router =  APIRouter( prefix="/Notes",tags=["Patient Notes Endpoint"])
db_dependency = Annotated[Session, Depends(get_db)]

# Fetch notes by note_ID
@notes_router.get("/by_id/{Id:str}",status_code=status.HTTP_200_OK)
def Fetch_by_notes_Id(db:db_dependency,Id:str):
    return get_patient_note_by_Id(db=db,Id=Id)

# Fetch notes by patient ID
@notes_router.get("/notes_by_patient_id/{patientId}/{Limit}/{Offset}",status_code=status.HTTP_200_OK)
def Fetch_notes_by_patient_id(db:db_dependency,Limit:int,Offset:int,patient_id:str):
    return get_patient_notes_by_patientID(db=db,patient_id=patient_id,limit=Limit,offset=Offset)

# Create new notes endpoint
@notes_router.post("/create",status_code=status.HTTP_201_CREATED)
def Create_new_notes_endpoint(db:db_dependency,new_record:patient_note_insert):
    return create_new_notes_record(db=db,record=new_record)

# Edit notes endpoint
@notes_router.patch("/edit",status_code=status.HTTP_200_OK)
def Edit_notes_endpoint(db:db_dependency,record:patient_note_edit):
    return edit_patient_note_record(db=db,record=record)