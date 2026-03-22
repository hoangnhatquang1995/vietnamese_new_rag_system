from langchain.tools import tool
from data.rss import request_rss_data,RSSParam

@tool
def fetch_news(catalogs: str, limit_article: int = 200):
    """
    Lấy tin tức từ trang vnexpress theo danh mục và số lượng bài viết yêu cầu.
    Args:
    - catalogs: Danh mục tin tức, cách nhau bằng dấu phẩy (ví dụ: "tin-moi-nhat,thoi-su").
    - limit_article: Số lượng bài viết tối đa cần lấy (mặc định là 200).
    Returns:
    - Một danh sách các bài viết, mỗi bài viết là một dict chứa thông tin về
    """
    catalog_list = [catalog.strip() for catalog in catalogs.split(",")]
    param = RSSParam(
        catalogs=catalog_list,
        limit_article=limit_article
    )
    articles = request_rss_data(param)
    return articles

tools = {
    "fetch_news": fetch_news
}