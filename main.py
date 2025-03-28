#Створити додаток FastAPI, який демонструє використання базової автентифікації за допомогою HTTPBasic.
#Реалізувати OAuth2 в додатку FastAPI.
#Створити маршрути для автентифікації через OAuth2, включаючи ендпойнт для отримання токена.

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBasic, HTTPBasicCredentials

app = FastAPI()

security = HTTPBasic()

@app.get("/basic-auth", summary="Basic Authentication", tags=["Authentication"])
def basic_auth(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != "user" or credentials.password != "password":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неправильне ім'я або пароль",
            headers={"WWW-Authenticate": "Basic"},
        )
    return {"username": credentials.username, "password": credentials.password}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

users_db = {}

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

@app.get("/users/me", summary="Get Current User", tags=["User"])
def read_users_me(token: str = Depends(oauth2_scheme)):
    username = users_db.get(token)
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неправильний токен",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"username": username}
