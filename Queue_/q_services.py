from modals.db_modals import Queue_table
from Queue_.q_class import QueueInsert, Queue
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


# Get all queue records from db
def get_queues(db:Session,limit:int,offset:int):
    return db.query(Queue_table).filter(
        Queue_table.created_at == func.now()
    ).limit(limit=limit).offset(offset=offset).all()

# Create Queue record
def create_queue(db:Session,create_queue:QueueInsert):
    try:

        New_Queue = Queue_table(appointment_id =  create_queue.appointment_id)
        db.add(New_Queue)
        db.commit()

        return "New Queue added"
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error adding new queue"
    )