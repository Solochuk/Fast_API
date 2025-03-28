from fastapi import HTTPException, status, Depends
from sqlmodel import select

from db import Config, User
from .ouath2 import oauth2_scheme
from main import app


@app.get("/users")
async def get_users(username: str, token = Depends(oauth2_scheme)):
    with Config.SESSION as session:
        users = session.exec(select(User).where(User.username == username)).all()
        if not users:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")
        return users

@app.get("/user")
async def get_user(username: str, token = Depends(oauth2_scheme)):
    with Config.SESSION as session:
        user = session.exec(select(User).where(User.username == username)).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No user found")
        return user

@app.post("/create_user", tags=["User"])
async def create_user(user: User):
    with Config.SESSION as session:
        user = session.exec(select(User).where(User.username == user.username)).first()
        if user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
        session.add(user)
        session.commit()
        session.refresh(user)
        return {f"User created successfully": user}

@app.put("/update_user", tags=["User"])
async def update_user(user: User, token: str = Depends(oauth2_scheme)):
    with Config.SESSION as session:
        db_user = session.exec(select(User).where(User.username == user.username)).first()
        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        db_user.username = user.username
        db_user.password = user.password
        db_user.email = user.email
        session.commit()
        session.refresh(db_user)
        return {f"User updated successfully": db_user}
