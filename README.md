# Vietnamese News RAG System

Hệ thống hỏi đáp tiếng Việt cho tin tức VnExpress theo hướng **RAG (Retrieval-Augmented Generation)**.

> Cập nhật README theo code hiện tại: **2026-03-31**

## 📋 Mô tả ngắn

Ứng dụng web cho phép:
- Fetch tin tức qua RSS (hiện tại: VnExpress) → lưu vào SQLite
- Ingest nội dung bài viết vào **vector store** để truy xuất theo ngữ nghĩa
- Hỏi đáp: hệ thống retrieve ngữ cảnh liên quan và yêu cầu LLM trả lời **chỉ dựa trên ngữ cảnh**

## 🚀 Tính năng & endpoint

**Web UI (Jinja2):**
- `GET /` Trang chủ
- `GET /news/` Danh sách bài báo trong SQLite
- `POST /news/fetch` Fetch RSS (mặc định 50 bài `tin-moi-nhat`) + ingest vào vector store
- `GET /rag/` Form hỏi đáp
- `POST /rag/ask` Hỏi đáp qua RAG chain (render HTML)

**Chat UI (Gradio):**
- `GET /gradio_chatbot_url` Giao diện chat Gradio (được mount trong FastAPI)

**JSON API:**
- `POST /rag/ask_json` Trả JSON
  - `use_agent=false`: chạy RAG chain trực tiếp (ổn định)
  - `use_agent=true`: hiện là **scaffold** (chưa implement đầy đủ, trả về chuỗi TODO)

Payload mẫu:
```json
{
  "question": "Tóm tắt các tin nổi bật gần đây",
  "use_agent": false,
  "include_trace": false
}
```

## 🧩 Kiến trúc (theo code)

```text
Browser
  |  GET /news/  -> đọc SQLite
  |  POST /news/fetch
  |     -> RSS VnExpress -> parse bài
  |     -> upsert SQLite (database.db)
  |     -> add vào VectorStore (Qdrant/Chroma)
  |
  |  POST /rag/ask hoặc /rag/ask_json
        -> Retriever(VectorStore) -> Context -> LLM -> Answer
```

## 📦 Yêu cầu hệ thống

- Python 3.10+ (khuyến nghị)
- Một LLM provider:
  - **DeepSeek Cloud** (mặc định theo code) hoặc
  - OpenAI / Google Gemini / Ollama (có sẵn connector trong `src/rag/llm.py`)
- **Qdrant** (mặc định theo code, chạy local qua Docker) *hoặc* chuyển sang Chroma local

## ⚙️ Cài đặt & chạy

1) Tạo env + cài dependencies
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

2) (Khuyến nghị) chạy Qdrant local
```bash
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

3) Tạo `.env` ở thư mục gốc (tối thiểu)
```env
# DeepSeek (mặc định theo src/rag/__init__.py)
DEEPSEEK_API_KEY=your_deepseek_api_key

# Qdrant (mặc định localhost:6333)
QDRANT_HOST=localhost
QDRANT_PORT=6333

# (tuỳ chọn) nếu bạn đổi LLM provider
OPENAI_API_KEY=
GOOGLE_API_KEY=
```

4) Chạy server
```bash
python src/main.py
```

5) Truy cập
- Web: http://localhost:8000
- News: http://localhost:8000/news/
- Ask: http://localhost:8000/rag/
- Gradio chat: http://localhost:8000/gradio_chatbot_url

## 🧠 Công nghệ chính

- FastAPI + Jinja2 templates
- SQLite + SQLModel (`database.db` ở thư mục gốc)
- LangChain (retrieval chain) + sentence-transformers embeddings (mặc định)
- Vector store: **Qdrant** (mặc định) / Chroma (có sẵn)
- Gradio ChatInterface (mount trong FastAPI)

## 📁 Cấu trúc thư mục (rút gọn)

```
src/
  api/                # FastAPI app + routes
  data/               # RSS + SQLite + vectorstore wrapper
  rag/                # Embedding + LLM + RAG chain (+ agent scaffold)
  settings/           # settings.py
templates/            # Jinja2 UI
statics/              # CSS
stored/               # persist cho Chroma (nếu dùng local)
database.db           # SQLite database (tạo khi chạy)
```

## 🛠️ Tuỳ chỉnh nhanh

- Embedding model, chunking: `src/settings/settings.py`
- Đổi vector store: `src/rag/__init__.py` (mặc định đang dùng `VectorStore.QDRANT`)
- Đổi LLM provider: `src/rag/__init__.py` / `src/rag/llm.py`

## 📌 Ghi chú

- `use_agent=true` trong `/rag/ask_json` hiện chưa hoàn thiện (agent nằm trong `src/rag/agent/`).

## Reference

https://medium.com/@codeawake/ai-chatbot-frontend-1823b9c78521