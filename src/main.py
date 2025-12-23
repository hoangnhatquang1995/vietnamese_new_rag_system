import data 
import rag

rss_datas = data.rss.request_rss_data(
    data.rss.RSSParam(
        catalogs=["tin-moi-nhat"]
    )
)

with open("rss_file.txt",mode = "w", encoding='utf8') as f:
    for data in rss_datas:
        f.write(f"[Document]{data['title']}\n")
        f.write(f"{data['content']}\n")