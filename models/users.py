from pydantic import BaseModel
from typing import Union, List

class User(BaseModel):
    name: str
    password: str