from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel, validator, Field
from datetime import date
from typing import List

app = FastAPI()

class Movie(BaseModel):
    id: int
    title: str = Field(..., description="Назва фільму")
    director: str = Field(..., description="Режисер фільму")
    release_year: int = Field(..., description="Рік випуску фільму")
    rating: float = Field(..., ge=0, le=10, description="Рейтинг фільму")

    @validator("release_year")
    def validate_release(value):
        current_year = date.today().year
        if value > current_year:
            raise ValueError('Рік випуску не може бути в майбутньому')
        return value

movies = [{
  "id": 1,
  "title": "string",
  "director": "string",
  "release_year": 2024,
  "rating": 10
}]

@app.get('/movies', response_model=List[Movie])
async def get_movies():
    return movies

@app.post('/movies', response_model=Movie)
async def add_movie(movie:Movie):
    movie.id = len(movies)+1
    movies.append(movie)
    return movie

@app.get('/movies{id}', response_model=Movie)
async def get_movie(id: int = Path(..., description="ID фільму")):
    for movie in movies:
        if movie['id'] == id:
            return movie
        else:
            raise HTTPException(status_code=404, detail="ФІльм не знайдено😥")

@app.delete('/movies{id}')
async def delet_movie(id: int = Path(..., description="ID фільму")):
    for movie in movies:
        if movie['id'] == id:
            movies.remove(movie)
            return {'message': 'ФІльм видалено'}
        else:
            raise HTTPException(status_code=404, detail="ФІльм не знайдено😥")
