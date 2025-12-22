from fastapi import Request, Response,FastAPI,Body,Header
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static",StaticFiles(directory="static/"),name="static")
