from fastapi import APIRouter, HTTPException, Form
from fastapi.responses import FileResponse
from pydantic import ValidationError
from app.api.model import User
from typing import List
from app.main import db


users = APIRouter()


@users.get("/", response_model=List[User])
async def get_users():
    return db


@users.get("/new_user")
async def form_for_user():
    return FileResponse("templates/new_user.html")


@users.post("/new_user", status_code=201)
async def add_user(
    name: str = Form(...),
    surname: str = Form(...),
    age: int = Form(...),
    rating: int = Form(...),
):
    try:
        new_user = User(name=name, surname=surname, age=age, rating=rating)
    except ValidationError:
        raise HTTPException(status_code=422)
    new_user = new_user.model_dump()
    db.append(new_user)
    return {"id": len(db) - 1}


@users.put("/{id}")
async def change_user(id: int, user: User):
    user = user.model_dump()
    if id in range(len(db)):
        db[id] = user
        return "ok"
    raise HTTPException(status_code=404, detail="wrong id")


@users.delete("/{id}")
async def delete_user(id: int):
    if id in range(len(db)):
        db.pop(id)
        return "ok"
    raise HTTPException(status_code=404, detail="wrong id")
