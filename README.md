# Vietnamese News RAG System

Hệ thống hỏi đáp thông minh về tin tức Việt Nam sử dụng công nghệ Retrieval-Augmented Generation (RAG).

## 📋 Mô tả dự án

Vietnamese News RAG System là một ứng dụng web cho phép người dùng:
- Thu thập tin tức mới nhất từ các nguồn RSS uy tín
- Đặt câu hỏi về các tin tức đã thu thập và nhận câu trả lời thông minh
- Tìm kiếm thông tin chính xác dựa trên dữ liệu tin tức thực tế

Hệ thống sử dụng công nghệ RAG (Retrieval-Augmented Generation) để đảm bảo câu trả lời chính xác và đáng tin cậy, chỉ dựa trên thông tin từ các bài báo đã thu thập.

## 🏗️ Kiến trúc hệ thống

```
vietnamese_new_rag_system/
├── src/
│   ├── api/              # API endpoints
│   ├── data/             # Xử lý dữ liệu và RSS
│   ├── rag/              # Hệ thống RAG
│   └── settings/         # Cấu hình hệ thống
├── templates/            # Giao diện web (Jinja2)
├── statics/              # Tài nguyên tĩnh (CSS, JS, images)
├── stored/               # Lưu trữ vector database
├── db/                   # Cơ sở dữ liệu SQLite
└── requirements.txt      # Các thư viện phụ thuộc
```

## 🚀 Tính năng chính

- **Thu thập tin tức tự động**: Lấy tin tức mới nhất từ các nguồn RSS
- **Hỏi đáp thông minh**: Trả lời câu hỏi dựa trên nội dung tin tức
- **Giao diện web thân thiện**: Dễ sử dụng với các tính năng trực quan
- **Hệ thống RAG**: Đảm bảo độ chính xác cao trong câu trả lời
- **Hỗ trợ tiếng Việt**: Hoạt động tốt với ngôn ngữ tiếng Việt

## 📦 Yêu cầu hệ thống

- Python 3.8+
- Pip (quản lý gói)
- Ollama (cho mô hình ngôn ngữ cục bộ) hoặc API key cho các dịch vụ đám mây

## ⚙️ Cài đặt

1. **Clone repository**:
   ```bash
   git clone <repository-url>
   cd vietnamese_new_rag_system
   ```

2. **Tạo môi trường ảo**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Trên Windows: .venv\Scripts\activate
   ```

3. **Cài đặt các thư viện cần thiết**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Cấu hình môi trường**:
   Tạo file `.env` trong thư mục gốc với các thông tin cần thiết:
   ```env
   # Nếu sử dụng Ollama
   OLLAMA_BASE_URL=http://localhost:11434
   
   # Nếu sử dụng Google Gemini
   GOOGLE_API_KEY=your_google_api_key
   
   # Nếu sử dụng OpenAI
   OPENAI_API_KEY=your_openai_api_key
   ```

5. **Chạy ứng dụng**:
   ```bash
   python src/main.py
   ```

6. **Truy cập ứng dụng**:
   Mở trình duyệt và truy cập `http://localhost:8000`

## 📖 Hướng dẫn sử dụng

1. **Thu thập tin tức**:
   - Truy cập trang "Tin tức" (`/news`)
   - Nhấn nút "Fetch RSS Mới" để thu thập tin tức mới nhất

2. **Hỏi đáp**:
   - Truy cập trang "Hỏi Tin tức" (`/rag`)
   - Nhập câu hỏi của bạn vào ô nhập liệu
   - Nhấn "Ask" để nhận câu trả lời dựa trên tin tức đã thu thập

## 🧠 Công nghệ sử dụng

- **Backend**: FastAPI
- **Frontend**: Jinja2 Templates, HTML, CSS
- **Cơ sở dữ liệu**: SQLite với SQLModel
- **Xử lý ngôn ngữ**: Langchain
- **Vector Database**: FAISS
- **Mô hình ngôn ngữ**: 
  - Ollama (local) - deepseek-r1
  - Google Gemini
  - OpenAI
- **Xử lý văn bản**: sentence-transformers

## 📁 Cấu trúc thư mục

```
src/
├── api/
│   ├── app.py          # Ứng dụng FastAPI chính
│   └── routes/
│       ├── news.py     # Route xử lý tin tức
│       └── rag.py      # Route xử lý hỏi đáp
├── data/
│   ├── database.py     # Mô hình dữ liệu
│   ├── rss.py          # Xử lý RSS feeds
│   └── sqldb.py        # Kết nối cơ sở dữ liệu
├── rag/
│   ├── documents.py    # Xử lý tài liệu
│   ├── embedding.py    # Xử lý embedding
│   ├── llm.py          # Kết nối LLM
│   ├── qa.py           # Xử lý hỏi đáp
│   └── vectorstore.py  # Vector database
└── settings/
    └── settings.py     # Cấu hình hệ thống
```

## 🛠️ Tùy chỉnh

Bạn có thể tùy chỉnh các thông số trong `src/settings/settings.py`:
- `EMBEDDING_MODEL`: Mô hình embedding sử dụng
- `LLM_MODEL`: Mô hình ngôn ngữ sử dụng
- `CHUNK_SIZE`: Kích thước đoạn văn bản chia nhỏ
- `CHUNK_OVERLAPPED`: Độ chồng giữa các đoạn văn bản

## 🙏 Lời cảm ơn

- Cảm ơn các nguồn RSS đã cung cấp dữ liệu tin tức
- Cảm ơn cộng đồng open-source đã cung cấp các thư viện hỗ trợ

## REFERENCE
https://medium.com/@codeawake/ai-chatbot-frontend-1823b9c78521