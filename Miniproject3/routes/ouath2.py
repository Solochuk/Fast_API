from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import select
from jose import jwt, JWTError
from datetime import datetime, timedelta

from db import Config, User
from main import app


SECRET = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/token/")
async def token(form: OAuth2PasswordRequestForm = Depends()):
    with Config.SESSION as session:
        user = session.exec(select(User).where(User.username == form.username)).first()
        if user:
            try:
                decoded = jwt.decode(user.password, SECRET, algorithms=[ALGORITHM])["password"]
                if decoded == form.password:
                    access_token = jwt.encode({"sub": user.username, "exp": datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE))}, SECRET, algorithm=ALGORITHM)
                    return{
                        "access_token": access_token,
                        "token_type": "bearer",
                        }
            except JWTError:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authority")
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authority")

@app.post("/registration/", summary="Registration for users", tags=["Registration"])
async def regist_user(user:User):
    jwt_token = jwt.encode({"password": user.password}, SECRET, algorithm=ALGORITHM)
    user.password = jwt_token

    with Config.SESSION as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
