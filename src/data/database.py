from . import sqldb
from .rss import RSSParam,request_rss_data
from sqlmodel import Session,select
from typing import List
from .types import Article

def db_create_article(article : Article, session : Session, update_if_exist = False):
    existing_article = session.get(Article,article.source)
    if existing_article and update_if_exist:
        db_update_article(
            source = article.source,
            article = article,
            session = session)
        return 
    session.add(article)
    session.commit()
    session.refresh(article)
    return 

def db_create_articles(articles : List[Article], session : Session, update_if_exist = False):
    for article in articles:
        existing_article = session.get(Article,article.source)
        if existing_article and update_if_exist:
            db_update_article(
                source = article.source,
                article = article,
                session = session)
            continue
        else:
            print(f"[ERROR] article {article} exist. Abort!")
            return 
        session.add(article)
    session.commit()
    return 

def db_update_article(source : str, article : Article, session : Session):
    # statement = select(Article).where(Article.source == source)
    existing_article = session.get(Article,source)

    if not existing_article:
        print(f"Article {source} not found")
        return None

    if article.title is not None:
        existing_article.title = article.title

    if article.published_time is not None:
        existing_article.published_time = article.published_time

    if article.content is not None:
        existing_article.content = article.content

    session.add(existing_article)
    session.commit()
    session.refresh(existing_article)

    return existing_article

def db_poluting_rss(param : RSSParam,session : Session):
    list = request_rss_data(param = param)
    articles:List[Article] = []
    for item in list:
        articles.append(Article.from_dictionary(item))
    db_create_articles(
        article= articles,
        session = session,
        update_if_exist= True
    )
    return articles
    
    
