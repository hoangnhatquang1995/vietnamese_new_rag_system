from fastapi import APIRouter,Depends,Request
from fastapi.templating import Jinja2Templates
from data.database import db_poluting_rss
from data.rss import RSSParam,request_rss_data
from data.sqldb import SessionDep
from data.types import Article
from sqlmodel import select
from rag import read_doc

router = APIRouter(
    prefix="/news",
    tags = ["news"]
)
templates = Jinja2Templates(directory="templates")

@router.get("/")
def news_page(request : Request, session: SessionDep):
    articles = session.exec(select(Article)).all()

    return templates.TemplateResponse(
        "news.html",
        {"request": request, "articles": articles}
    )

@router.post("/fetch")
def fetch_news(session: SessionDep):
    param = RSSParam(
        catalogs=["tin-moi-nhat"],
        limit_article=50
    )
    articles = db_poluting_rss(param, session)
    list = [ article.model_dump() for article in articles ]
    read_doc(list)
    return {
        "count": len(articles),
        "list" : list
    }
