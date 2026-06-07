from pydantic import BaseModel


class Queue(BaseModel):
    queue_id:str
    appointment_id:str
    created_at:str

class QueueInsert(BaseModel):
    appointment_id:str