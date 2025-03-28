from typing import Optional
from sqlmodel import Relationship, SQLModel, Field
from pydantic import field_validator



class Advertisement(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    category: str
    price: float
    user_id: int = Field(foreign_key="user.id")

    user: "User" = Relationship(back_populates="advertisements")

    @field_validator('title')
    @classmethod
    def title_val(cls, v):
        if " " in v:
            raise ValueError("title must not contain a space")
        return v

    @field_validator('description')
    @classmethod
    def description_val(cls, v):
        if " " in v:
            raise ValueError("description must not contain a space")
        return v

    @field_validator('price')
    @classmethod
    def price_val(cls, v):
        if v <= 0:
            raise ValueError("price must be a positive number")
        return v
