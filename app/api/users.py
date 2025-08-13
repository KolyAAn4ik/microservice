from fastapi import APIRouter, HTTPException
from app.api.model import User
from typing import List


db = []
users = APIRouter()


@users.get('/', response_model=List[User])
async def get_users():
    return db

@users.post('/', status_code=201)
async def add_user(new_user: User):
    new_user = new_user.model_dump()
    db.append(new_user)
    return {'id': len(db) - 1}

@users.put('/{id}')
async def change_user(id: int, user: User):
    user = user.model_dump()
    if id in range(len(db)):
        db[id] = user
        return "ok"
    raise HTTPException(status_code=404, detail="wrong id")

@users.delete('/{id}')
async def delete_user(id: int):
    if id in range(len(db)):
        db.pop(id)
        return "ok"
    raise HTTPException(status_code=404, detail='wrong id')

