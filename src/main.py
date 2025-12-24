import data 
from rag.documents import to_list_documents,chunking_document
from rag.embedding import EmbeddingProvider,get_embedding_provider
from rag import db
from grade import relevent
from rag.llm import get_llm,LLM
from rag.qa import build_rag_chain

from settings.settings import HUGGINGFACE_MODEL_NAME
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai.chat_models import ChatGoogleGenerativeAIError

rss_datas = data.rss.request_rss_data(
    data.rss.RSSParam(
        catalogs=["tin-moi-nhat"],
    )
)
with open("rss_scrap.txt",mode = "w",encoding="utf8") as f:
    for d in rss_datas:
        f.write(f"[{d['source']}]\n{d['content']}\n")
    
def show_context(context):
    """
    Display the contents of the provided context list.

    Args:
        context (list): A list of context items to be displayed.

    Prints each context item in the list with a heading indicating its position.
    """
    for i, c in enumerate(context):
        print(f"Context {i + 1}:")
        print(c)
        print("\n")

documents = to_list_documents(rss_datas)
chunk = chunking_document(documents)
embedding = get_embedding_provider(EmbeddingProvider.HUGGING_FACE,HUGGINGFACE_MODEL_NAME)
db.load(
    embedder = embedding
)
db.add(chunk)
retriever = db.retriver()

llm = get_llm(LLM.Local.OLLAMA , "deepseek-r1")
rag_chain = build_rag_chain(llm,retriever)
try :
    answer= rag_chain.invoke({"input": "Bạn hãy cho tôi thông tin về Phạm Nhật Vượng"})
    print(answer['answer'])
except ChatGoogleGenerativeAIError as e:
    print(f" e = {e}")