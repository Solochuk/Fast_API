from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field, validator
from datetime import datetime

app = FastAPI()

class User(BaseModel):
    name: str = Field(..., title="Ім'я")
    email: str = Field(..., title="Email")
    age: int = Field(..., title="Вік")

    @validator("email")
    @classmethod
    def email_validator(cls, email):
        if "@" not in email:
            raise ValueError("Неправильний формат email")
        return email

    @validator("age")
    @classmethod
    def age_validator(cls, age):
        if age < 14:
            raise ValueError("Вік повинен бути більше 14")
        return age

class Article(BaseModel):
    id: int
    title: str = Field(..., title="Заголовок")
    text: str = Field(..., title="Текст")
    author: User = Field(..., title="Автор")
    comments: list = Field(..., title="Коментарі")
    creat_date: str = Field(..., title="Дата створення")

    @validator("creat_date")
    @classmethod
    def creat_date_validator(cls, creat_date):
        date = datetime.strptime(creat_date, "%Y-%m-%d")
        if date > datetime.now():
            raise ValueError("Дата не може бути в майбутньому")
        return creat_date



    @validator("text")
    @classmethod
    def text_validator(cls, text):
        if len(text) < 10:
            raise ValueError("Текст повинен бути більше 10 символів")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

users_db = {}

articles_db = {
    1: {
        "id": 1,
        "title": "asda",
        "text": "stasdaring",
        "author": {
            "name": "striasdng",
            "email": "string@",
            "age": 23
        },
        "comments": [
            "adaasdad"
        ],
        "creat_date": "2024-12-13"
    }
}

@app.post("/token", summary="OAuth2 Token", tags=["Authentication"])
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != "user" or form_data.password != "password":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неправильне ім'я або пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = form_data.username + "123"
    users_db[token] = form_data.username
    return {"access_token": token, "token_type": "bearer"}

@app.get("/articles/{id}", summary="Get Article", tags=["Article"])
def get_article(id: int):
    article = articles_db.get(id)
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Стаття не знайдена"
        )
    return article

@app.get("/articles/", summary="Get Articles", tags=["Article"])
def get_articles():
    return articles_db

@app.post("/article/", summary="Create Article", tags=["Article"])
def create_article(article: Article, token: str = Depends(oauth2_scheme)):
    if token not in users_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неправильний токен",
            headers={"WWW-Authenticate": "Bearer"},
        )
    for article_all in articles_db.values():
        if article_all["title"] == article.title:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Стаття з таким заголовком вже існує"
            )
    article.id = max(articles_db.keys(), default=0) + 1
    articles_db[article.id] = article.dict()
    return {"message": "Стаття створена", "article_id": article.id}
