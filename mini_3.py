from fastapi import FastAPI
from pydantic import BaseModel, validator, Field
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine("sqlite://", echo=True)
session = Session(engine)

app = FastAPI()

class User(BaseModel):
    id: int``
    name:str = Field(..., titlle = 'Ім\'я користувача')
    email: str = Field(..., titlle="Електронна адреса")
    password: str = Field(..., titlle="Пароль", min_length=8)

    @validator('email')
    @classmethod
    def validatte_email(cls, email):
        if '@' not in email:
            raise ValueError('Неправильний формат електронної адреси')
        return email

    @validator('password')
    @classmethod
    def validate_password(cls, password):
        if len(password) < 8:
            raise ValueError('Пароль повинен бути не менше 8 символів')
        return password

class Announcement(BaseModel):
    id: int
    name: str = Field(..., titlle="Назва продукту")
    price: float = Field(..., titlle="Ціна продукту")
    seller: User
    description:str = Field(..., titlle="Опис продукту")
