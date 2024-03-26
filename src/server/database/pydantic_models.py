from pydantic import BaseModel
from typing import Optional


class ModifyBaseModel(BaseModel):
    id: Optional[int] = 0


class ChangePassword(ModifyBaseModel):
    password: str


class LoginData(ModifyBaseModel):
    login: str
    password: str


class User(ModifyBaseModel):
    position: str
    login: str
    password: str
    power_level: int 

class Workers(ModifyBaseModel):
    post_id: int
    name: str
    surname: str
    telephone_number: str

class Post(ModifyBaseModel):
    post: str

class Services(ModifyBaseModel):
    name: str
    price: str
    description: str

class Client(ModifyBaseModel):
    name: str
    address: str
    telephone_number: str

class Visits(ModifyBaseModel):
    visit_id: int
    client_id: int
    service_id: int
    worker_id: int
    datetime: str
    