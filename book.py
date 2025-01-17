from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, validator, Field
from datetime import datetime
from typing import List, Optional

app = FastAPI()

books = []
users = []
events = []

class Book(BaseModel):
    id: int
    name: str = Field(..., description="Назва книги")
    autor: str = Field(..., description="Автор книги")
    year: int = Field(..., description="Рік видання книги")
    amout: int = Field(..., description="Кількість книг")

@app.get('/books', response_model=List[Book])
def get_books():
    return books

@app.post('/books', response_model=Book, status_code=status.HTTP_201_CREATED)
def add_book (book: Book):
    book.id = len(books) + 1
    books.append(book)
    return book

@app.get('/books/{id}', response_model=Book)
def get_book(id: int):
    for book in books:
        if book.id == id:
            return book
        else:
            raise HTTPException(status_code=404, detail="Книгу не знайдено")

class User(BaseModel):
    id: int
    name: str = Field(...,min_length=2, description="Ім'я користувача")
    email: str = Field(...,min_length=2, description="Електронна пошта користувача")
    password: str = Field(..., description="Пароль користувача")
    phone: str = Field(..., description="Телефон користувача")

    @validator("email")
    def validate_email(value):
        if '@' not in value:
            raise ValueError('Невалідна електронна пошта')
        return value

    @validator("password")
    def validate_password(value):
        if len(value) < 8:
            raise ValueError('Пароль закороткий')
        if not any(c.isupper() for c in value):
            raise ValueError('Пароль повинен містити хоча б одну велику літеру')
        if not any(c.islower() for c in value):
            raise ValueError('Пароль повинен містити хоча б одну маленьку літеру')
        if not any(c.isdigit() for c in value):
            raise ValueError('Пароль повинен містити хоча б одну цифру')
        if not any(c in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~" for c in value):
            raise ValueError('Пароль повинен містити хоча б один спеціальний символ')
        return value

    @validator("phone")
    def validate_phone(value):
        if "+380" not in value:
            raise ValueError('Невалідний номер телефону')

@app.post('/users', response_model=User, status_code=status.HTTP_201_CREATED)
def add_user(user: User):
    user.id = len(users) + 1
    users.append(user)
    return user
