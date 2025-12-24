from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from rag import read_doc,chat
router = APIRouter(
    prefix="/rag",
    tags = ["rag"]
)
templates = Jinja2Templates(directory="templates")

@router.get("/")
def ask_page(request: Request):
    return templates.TemplateResponse(
        "ask.html",
        {"request": request}
    )


@router.post("/ask")
def ask_news(
    request: Request,
    question: str = Form(...)
):
    result = chat(question)
    print(f"Result = {result}")
    return templates.TemplateResponse(
        "ask.html",
        {
            "request": request,
            "question": question,
            "answer" : result,
            "sources": ["vnexpress"]
        }
    )
