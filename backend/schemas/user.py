from pydantic import BaseModel
from fastapi import Form

class UserCreate(BaseModel):

    username: str =Form(),

    password: str=Form(),

    email: str=Form(),

class UserLogin(BaseModel):
    username: str=Form(),
    password: str=Form(),