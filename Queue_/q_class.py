from pydantic import BaseModel


class Queue(BaseModel):
    queue_id:str
    appointment_id:str
    slot_number:int
    created_at:str

class QueueInsert(BaseModel):
    appointment_id:str