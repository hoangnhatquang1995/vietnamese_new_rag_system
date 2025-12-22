from typing import Annotated,Optional,List
from sqlmodel import SQLModel,Field,Session

from langchain_classic.schema import Document

class Article(SQLModel,table = True):
    url: Optional[str]              =   Field(default=None,primary_key= True)
    title: Optional[str]            =   Field(index = True)
    published_time: Optional[str]   =   Field()
    content: Optional[str]          =   Field()
    
    @classmethod
    def from_dictionary(cls,dic : dict) :
        return cls(
            url = dic["url"],
            title = dic["title"],
            published_time = dic["published_time"],
            content = dic["formatted_content"]
        )
    
class ArticleDocument(Document) :
    def __init__(
        self,
        url: str,
        title: str,
        published_time: str,
        content: str,
        images: Optional[List[str]] = None,
        **kwargs
    ):
        super().__init__(
            page_content=content,
            metadata={
                "url": url,
                "title": title,
                "published_time": published_time,
                "images": images or [],
                "source": "vnexpress",
            },
            **kwargs
        )

    @classmethod
    def from_dict(cls, data: dict) -> "Article":
        return cls(
            url=data.get("url", ""),
            title=data.get("title", ""),
            published_time=data.get("published_time", ""),
            content=data.get("content", ""),
            images=data.get("images", []),
        )

    @property
    def title(self) -> str:
        return self.metadata.get("title", "")

    @property
    def url(self) -> str:
        return self.metadata.get("url", "")

    @property
    def published_time(self) -> str:
        return self.metadata.get("published_time", "")

    @property
    def images(self) -> List[str]:
        return self.metadata.get("images", [])

    @property
    def content(self) -> str:
        return self.get_content()
        

    def __repr__(self) -> str:
        return f"Article(title='{self.title}', url='{self.url}')"
