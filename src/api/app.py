from fastapi import Request, Response,FastAPI,Body,Header
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates
import os
from .routes import news,rag

templates = Jinja2Templates(directory="templates")

app = FastAPI()
    
app.mount("/statics",StaticFiles(directory="statics/"),name="statics")

app.include_router(news.router)
app.include_router(rag.router)

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )
