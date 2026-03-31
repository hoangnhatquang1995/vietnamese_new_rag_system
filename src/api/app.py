from fastapi import Request, Response,FastAPI,Body,Header
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates
import os
from .routes import news,rag
from data.sqldb import create_db_and_tables
from rag import read_doc,chat

import gradio as gr 

templates = Jinja2Templates(directory="templates")

app = FastAPI()
    
app.mount("/statics",StaticFiles(directory="statics/"),name="statics")

app.include_router(news.router)
app.include_router(rag.router)


@app.on_event("startup")
def _startup_create_tables() -> None:
    create_db_and_tables()

gradio_app = gr.ChatInterface(
    fn=chat,
    title="Vietnamese News RAG Chatbot",
    description="Ask questions about Vietnamese news and get intelligent answers from the system.",
)
app = gr.mount_gradio_app(app, gradio_app, path="/gradio_chatbot_url")

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
        }
    )
