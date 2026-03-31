from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from rag import read_doc,chat
from pydantic import BaseModel
from rag.agent import run_agent

router = APIRouter(
    prefix="/rag",
    tags = ["rag"]
)
templates = Jinja2Templates(directory="templates")


class AskJsonRequest(BaseModel):
    question: str
    use_agent: bool = True
    include_trace: bool = False

@router.get("/")
def ask_page(request: Request):
    return templates.TemplateResponse(
        "ask.html",
        {
            "request": request,
            "gradio_chatbot_url": "/gradio_chatbot_url",
        }
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


@router.post("/ask_json")
def ask_news_json(payload: AskJsonRequest):
    question = (payload.question or "").strip()
    if not question:
        response = {"answer": "", "sources": []}
        if payload.include_trace:
            response["trace"] = []
        return response

    if payload.use_agent:
        result = run_agent(question, include_trace=payload.include_trace)
        return result

    # Fallback: run the existing retrieval chain directly (HTML route uses this already).
    answer = chat(question)
    response = {"answer": answer, "sources": []}
    if payload.include_trace:
        response["trace"] = [{"type": "mode", "value": "rag_chain"}]
    return response
