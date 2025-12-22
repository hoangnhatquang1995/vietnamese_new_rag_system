from llama_index.core import Document
from typing import Annotated,Optional,List

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
    def from_dict(cls, data: dict):
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

def to_list_documents(dicts : List[dict]):
    docs = []
    for dict in dicts:
        docs.append(ArticleDocument.from_dict(dict))
    return docs