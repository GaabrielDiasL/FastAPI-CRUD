from pydantic import BaseModel, Field
from typing import Union, List

class User(BaseModel):
    username: str = Field('username_example', description="This is the username")
    password: str  = Field('password_example', description="This is the password field")
    name: str  = Field('Complete Name Example', description="This is the complete name field")
    system_admin: bool  = Field(True, description="Admin or not")

class UpdateUser(BaseModel):
    username: Union[str, None] = Field('username_example', description="This is the username")
    name: Union[str, None] = Field('Complete Name Example', description="This is the complete name field")