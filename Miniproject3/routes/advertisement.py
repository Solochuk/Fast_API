from fastapi import HTTPException, status, Depends
from sqlmodel import select

from db import Config, User, Advertisement
from .ouath2 import oauth2_scheme
from main import app


@app.get("/advertisements", tags=["Advertisement"])
async def get_advertisements(category: str, token: str = Depends(oauth2_scheme)):
    with Config.SESSION as session:
        advertisements = session.exec(select(Advertisement).where(Advertisement.category == category)).all()
        if not advertisements:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No advertisements found")
        return advertisements

@app.get("/advertisement", tags=["Advertisement"])
async def get_advertisement(id: int, token: str = Depends(oauth2_scheme)):
    with Config.SESSION as session:
        advertisement = session.exec(select(Advertisement).where(Advertisement.id == id)).first()
        if not advertisement:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Advertisement not found")
        return advertisement

@app.post("/create_advertisement", tags=["Advertisement"])
async def create_advertisement(advertisement: Advertisement, token: str = Depends(oauth2_scheme)):
    with Config.SESSION as session:
        session.add(advertisement)
        session.commit()
        session.refresh(advertisement)
        return {f"Advertisement created successfully": advertisement}

@app.put("/update_advertisement", tags=["Advertisement"])
async def update_advertisement(advertisement: Advertisement, token: str = Depends(oauth2_scheme)):
    with Config.SESSION as session:
        db_advertisement = session.exec(select(Advertisement).where(Advertisement.id == advertisement.id)).first()
        if not db_advertisement:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Advertisement not found")
        db_advertisement.title = advertisement.title
        db_advertisement.description = advertisement.description
        db_advertisement.category = advertisement.category
        db_advertisement.price = advertisement.price
        session.commit()
        session.refresh(db_advertisement)
        return {f"Advertisement updated successfully": db_advertisement}

@app.delete("/delete_advertisement", tags=["Advertisement"])
async def delete_advertisement(id: int, token: str = Depends(oauth2_scheme)):
    with Config.SESSION as session:
        advertisement = session.exec(select(Advertisement).where(Advertisement.id == id)).first()
        if not advertisement:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Advertisement not found")
        session.delete(advertisement)
        session.commit()
        return {f"Advertisement deleted successfully": advertisement}
