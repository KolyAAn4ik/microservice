from fastapi import FastAPI
db = []
from app.api.users import users
from app.api.http_files import http_file
from logs.logger import logger
from app.core.config import load_config

app = FastAPI()
app.include_router(users)
app.include_router(http_file)


@app.get("/db")
async def get_db_info():
    config = load_config()
    logger.info(f"Connecting to database: {config.db.database_url}")
    return {"database_url": config.db.database_url}
