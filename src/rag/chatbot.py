from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

from . import vectorstore

system_prompt = (
        """
    Bạn là trợ lý AI chuyên trả lời câu hỏi dựa trên các bài báo tiếng Việt.

    QUY TẮC:
    - Chỉ sử dụng thông tin trong NGỮ CẢNH.
    - Không suy đoán, không thêm kiến thức bên ngoài.
    - Nếu không có thông tin, trả lời:
      "Không tìm thấy thông tin này trong các bài viết được cung cấp."

    NGỮ CẢNH:
    {context}

    CÂU HỎI:
    {input}

    TRẢ LỜI (tiếng Việt):
    """

)
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])


def build_rag_chain(llm,retriever):
    print(f"llm = {llm} retriever = {retriever}")
    question_answer_chain = create_stuff_documents_chain(
        llm, 
        prompt
    )
    rag_chain = create_retrieval_chain(
        retriever, 
        question_answer_chain
    )
    return rag_chain