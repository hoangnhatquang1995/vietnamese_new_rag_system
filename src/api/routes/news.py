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
    print(f"articles = {len(articles)}")
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
    datas = request_rss_data(param = param)
    articles = db_poluting_rss(datas, session)
    read_doc(datas)
    return {
        "count": len(articles),
        "list" : articles
    }
   
