from typing import Annotated,Optional,List
from sqlmodel import SQLModel,Field,Session

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
    
