from modals.db_modals import Queue_table
from Queue_.q_class import QueueInsert, Queue
from sqlalchemy import asc
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


# Get all queue records from db
def get_queues(db:Session,limit:int,offset:int):
    return db.query(Queue_table).filter(
       asc(Queue_table.created_at)
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

# NEW: Dequeue the next appointment
def dequeue_appointment(db:Session):
    try:
        # 1. Find the oldest record. 
        # with_for_update(skip_locked=True) prevents race conditions if two 
        # workers try to dequeue at the exact same millisecond.
        next_in_line = db.query(Queue_table)\
            .order_by(asc(Queue_table.created_at))\
            .with_for_update(skip_locked=True)\
            .first()

        if not next_in_line:
            return None # Queue is empty

        # 2. Store the ID so we can return it
        completed_appointment_id = next_in_line.appointment_id

        # 3. Remove it from the queue
        db.delete(next_in_line)
        db.commit()

        return "Appointment Removed from Queue."

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error dequeuing appointment"
        )