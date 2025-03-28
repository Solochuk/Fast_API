from typing import Optional, List
from sqlmodel import Relationship, SQLModel, Field
from pydantic import field_validator, EmailStr
import re


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password:str
    email: EmailStr

    advertisements: List["Advertisement"] = Relationship(back_populates="user")

    @field_validator('username')
    def username_val(cls, v):
        if " " in v:
            raise ValueError("username must not contain a space")
        return v

    @field_validator('password')
    def password_val(cls, v):
        if " " in v:
            raise ValueError("password must not contain a space")
        if not re.search(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"):
            raise ValueError("password must contain at least 8 characters, including uppercase, lowercase, number and special character")
        return v

    @field_validator('email')
    def email_val(cls, v):
        if "@" not in v:
            raise ValueError("email must contain @ symbol")
        return v
