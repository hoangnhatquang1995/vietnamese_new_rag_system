from fastapi import Request, Response,FastAPI,Body,Header
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates
import os
from .routes import news,rag
from data.sqldb import create_db_and_tables

templates = Jinja2Templates(directory="templates")

app = FastAPI()
    
app.mount("/statics",StaticFiles(directory="statics/"),name="statics")

app.include_router(news.router)
app.include_router(rag.router)


@app.on_event("startup")
def _startup_create_tables() -> None:
    create_db_and_tables()

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )
