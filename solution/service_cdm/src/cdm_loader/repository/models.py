from pydantic import BaseModel

class MessageConsumerObj(BaseModel):
    object_id: int
    object_type: str
    payload: dict