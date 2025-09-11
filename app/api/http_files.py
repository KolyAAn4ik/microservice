from fastapi import FastAPI, File, UploadFile, APIRouter, Request
import aiofiles
from app.api.model import User
from app.main import db
from pydantic import ValidationError
from fastapi.templating import Jinja2Templates

http_file = APIRouter()
templates = Jinja2Templates(directory="templates")

@http_file.get("/new_file")
async def get_file(request: Request):
    return templates.TemplateResponse(
        "new_file.html",
        {
            "request": request
        }
    )

@http_file.post("/new_file")
async def post_file(request: Request, file: UploadFile):
    async with aiofiles.open(file.filename, "wb") as f:
        while chunk := await file.read(1024):
            await f.write(chunk)
    async with aiofiles.open(file.filename, "r") as f:
        lines = await f.readlines()
        lines = [line.strip() for line in lines]
    try:
        new_user = User(name=lines[0], surname=lines[1],
                        age=int(lines[2]), rating=int(lines[3]))
    except ValidationError:
        return templates.TemplateResponse(
            "new_file.html",
            {
                "request": request,
                "error": True,
                "message": "Неправильный ввод"
            }
        )
    new_user = new_user.model_dump()
    db.append(new_user)
    return templates.TemplateResponse(
            "new_file.html",
            {
                "request": request,
            }
        )
