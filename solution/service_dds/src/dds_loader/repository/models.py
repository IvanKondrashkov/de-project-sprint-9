from typing import List
from uuid import UUID
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

class ProductCategoryObj(BaseModel):
    user_id: UUID
    product_id: UUID
    category_id: UUID
    product_name: str
    category_name: str
    order_cnt: int

class MessageConsumerObj(BaseModel):
    object_id: int
    object_type: str
    payload: dict

class MessageProducerObj(BaseModel):
    object_id: int
    object_type: str
    payload: ProductCategoryObj