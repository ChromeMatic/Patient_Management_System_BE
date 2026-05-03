from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Session
from typing import Annotated
from database_config.db_config import get_db

queue_endpoint = APIRouter( prefix="/Queue",tags=["Queue Endpoint"])
db_dependency = Annotated[Session, Depends(get_db)]


@queue_endpoint.get("/all",status_code=status.HTTP_200_OK)
def Fetch_all_queues(db:db_dependency):
    return "Testing"