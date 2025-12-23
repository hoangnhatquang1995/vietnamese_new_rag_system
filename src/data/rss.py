## Source : https://gist.github.com/earlwlkr/e0f8fd602ae4f261f8ce 
# Python code to parse news content from VnExpress RSS Feeds.
import os
import re
from bs4 import BeautifulSoup   # external lib
import requests                 # external lib
import feedparser               # external lib
from datetime import datetime,timedelta
from typing import Annotated, List,Optional

rss_re = re.compile(r'/rss/[a-z-?]+.rss', flags=re.UNICODE)
word_re = re.compile('(\w+)', flags=re.UNICODE)  # Chưa chính xác.

parsed_rss = []

stop = False

main_url = 'http://vnexpress.net'
main_soup = BeautifulSoup(requests.get(main_url + '/rss').content,features="html.parser")
session = requests.Session()

class RSSParam :
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    catalogs : Optional[List[str]] = None
    limit_article : Optional[List[int]] = 200

    def __init__(self, start_date = None ,end_date = None,catalogs= None,limit_article = 200):
        self.start_date = start_date
        self.end_date = end_date
        self.catalogs = catalogs
        self.limit_article = limit_article
        
    @classmethod
    def lastest(cls,days : int = 0):
        end = datetime.now().astimezone()
        start = end - timedelta(days=days)
        return cls(
            start_date = start,
            end_date = end
        )
 
def to_pub_date(pub_date_str: str) -> Optional[datetime]:
    try:
        return datetime.strptime(pub_date_str, "%a, %d %b %Y %H:%M:%S %z")
    except Exception:
        return None

def parse_article(soup: BeautifulSoup, html: str):
    # soup = BeautifulSoup(html, "html.parser")

    title_el = soup.select_one("h1.title-detail")
    title = title_el.get_text(strip=True) if title_el else "No title"

    time_el = soup.select_one("span.date")
    published_time = time_el.get_text(strip=True) if time_el else ""

    # Content
    body_el = soup.select_one("article.fck_detail")
    paragraphs = []
    if body_el:
        for p in body_el.select("p"):
            text = p.get_text(" ", strip=True)
            if text:
                paragraphs.append(text)
    content = "\n\n".join(paragraphs)

    # Images
    images = []
    for img in soup.select("article.fck_detail img"):
        src = img.get("src") or img.get("data-src") or ""
        if src.startswith("//"):
            src = "https:" + src
        if src:
            images.append(src)

    og = soup.select_one('meta[property="og:image"]')
    if og:
        og_url = og.get("content")
        if og_url:
            images.insert(0, og_url)

    return {
        "url" : html,
        "title": title,
        "published_time": published_time,
        "content": content,
        "images": images,
    }


def request_rss_data(param: Optional[RSSParam] = None):
    list = []
    stop = False
    parsed_links = []
    index = 0
    # Lọc tất cả link trong trang RSS gốc để tìm link RSS.
    for a in main_soup.find_all('a'):
        if 'href' in a.attrs and rss_re.match(a['href']):
            catalog = a['href'].removeprefix("/rss/").removesuffix(".rss")
            if param is not None and catalog not in param.catalogs:
                continue
            print(f"[INFOR] Request get Catalog {catalog}")
            rss_link = main_url + a['href']

            if rss_link not in parsed_rss:
                print('Parsing RSS: ' + rss_link)
                feed = feedparser.parse(rss_link)
                items = feed['items']

                for item in items:
                    try:
                        index +=1
                        link = item['link']
                        if link in parsed_links:
                            continue

                        print('Parsing article: ' + link)
                        content = session.get(link).content
                        soup = BeautifulSoup(content)
                        article = parse_article(soup = soup, html= link)
                        list.append(article)
                        parsed_links.append(link)
                        if param is not None and param.limit_article is not None and len(parsed_links) >= param.limit_article:
                            print("EXCEED LIMIT")
                            stop = True
                            break
                    except Exception as e:
                        print(f'Error ({e}), skipping...')
                        continue
                   
                    if stop:
                        break
                parsed_rss.append(rss_link)
            if stop:
                break
    print('\n\nParsed a total of {0} articles.'.format(len(parsed_links)))
    return list

def request_rss_data_last(days: int) :
    end = datetime.now().astimezone()
    start = end - timedelta(days=days)
    return request_rss_data(start,end)

