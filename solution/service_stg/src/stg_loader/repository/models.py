from typing import List
from datetime import datetime
from pydantic import BaseModel

class UserObj(BaseModel):
    id: str
    name: str
    login: str

class RestaurantObj(BaseModel):
    id: str
    name: str

class ProductObj(BaseModel):
    id: str
    price: float
    quantity: int
    name: str
    category: str

class OrderObj(BaseModel):
    id: int
    date: datetime
    cost: float
    payment: float
    status: str
    restaurant: RestaurantObj
    user: UserObj
    products: List[ProductObj]

class MessageConsumerObj(BaseModel):
    object_id: int
    object_type: str
    sent_dttm: datetime
    payload: dict

class MessageProducerObj(BaseModel):
    object_id: int
    object_type: str
    payload: OrderObj  