from modals.db_modals import Queue_table
from Queue_.q_class import QueueInsert, Queue
from sqlalchemy import asc
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


# Get all queue records from db
def get_queues(db:Session,limit:int,offset:int):
    query = db.query(Queue_table).order_by(asc(Queue_table.created_at))
    queue_data = query.limit(limit=limit).offset(offset=offset).all()
    return queue_data

# Get queue by Id
def get_queue_by_id(db:Session,Id:str):
    return db.query(Queue_table).filter(Queue_table.queue_id == Id).first()

# Create Queue record
def create_queue(db:Session,create_queue:QueueInsert):
    try:

        New_Queue = Queue_table(
            appointment_id =  create_queue.appointment_id,
            slot_number = create_queue.slot_number
        )
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

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error dequeuing appointment"
        )

# delete from queue
def delete_queue_record(db:Session, queue_id:str):
    try:
        queue_rec = get_queue_by_id(db=db,Id=queue_id)

        if queue_rec is not None:
            db.delete(queue_rec)
            return "Recorded Deleted"
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Error"
            )
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Operation Failed"
        )