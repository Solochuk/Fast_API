from fastapi import FastAPI, HTTPException
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, validator, Field

app = FastAPI()

class Order(BaseModel):
    id: int
    name: str= Field(..., description="Назва товару")
    price: float= Field(..., description="Ціна товару")
    amount: int= Field(..., description="Кількість товару")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Дата створення замовлення")

    @validator("price")
    def validate_price(cls, value):
        if value <= 0:
            raise ValueError('Ціна товару не може бути від`ємною')
        return value

    @validator("amount")
    def validate_amount(cls, value):
        if value <= 0:
            raise ValueError('Кількість товару не може бути від`ємною')
        return value

class User(BaseModel):
    id: int
    name: str= Field(..., description="Ім'я користувача")
    email: str= Field(..., description="Електронна пошта користувача")
    list_of_orders: List[Order] = Field(..., description="Список замовлень користувача")

    @validator("email")
    def validate_email(cls, value):
        if '@' not in value:
            raise ValueError('Некоректна електронна пошта')
        return value

users=[]

@app.post("/users/")
def create_user(user: User):
    user.id = len(users) + 1
    for order in user.list_of_orders:
        order.id = len(users) + 1
    users.append(user)
    return user

@app.get("/users/")
def get_users(email: Optional[str] = None):
    if email:
        for user in users:
            if user.email == email:
                return user
        raise HTTPException(status_code=404, detail="Користувача не знайдено😥")
    return users
