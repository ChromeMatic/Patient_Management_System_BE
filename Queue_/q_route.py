from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Session
from typing import Annotated
from database_config.db_config import get_db
from Queue_.q_class import QueueInsert, Queue
from Queue_.q_services import get_queues, create_queue

queue_endpoint = APIRouter( prefix="/Queue",tags=["Queue Endpoint"])
db_dependency = Annotated[Session, Depends(get_db)]


@queue_endpoint.get("/all/{Limit:int}/{Offset:int}",status_code=status.HTTP_200_OK)
def Fetch_all_queues(db:db_dependency,Limit:int,Offset:int):
    return get_queues(db=db,limit=Limit,offset=Offset)

@queue_endpoint.post("/create",status_code=status.HTTP_200_OK)
def Create_new_queue(db:db_dependency,new_queue:QueueInsert):
    return create_queue(db=db,create_queue=new_queue)