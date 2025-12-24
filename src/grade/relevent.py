from rag.llm import *
from pydantic import BaseModel,Field
from langchain_core.prompts import ChatPromptTemplate
from typing import Literal
from settings.settings import LLM_MODEL

class GradeDocuments(BaseModel):
    """Binary score for relevance check on retrieved documents."""

    relevant: Literal["yes", "no"] = Field(
        description="Tài liệu có liên quan đến câu hỏi hay không?"
    )

SYSTEM_PROMPT = """Bạn là một hệ thống đánh giá mức độ liên quan của tài liệu được truy xuất
đối với câu hỏi của người dùng.

NGUYÊN TẮC:
- Nếu tài liệu có chứa từ khóa HOẶC ý nghĩa ngữ nghĩa liên quan đến câu hỏi → đánh giá là CÓ liên quan.
- Không cần đánh giá quá nghiêm ngặt.
- Mục tiêu là loại bỏ các tài liệu truy xuất SAI hoặc KHÔNG LIÊN QUAN.
- Chỉ trả lời bằng một từ duy nhất: "yes" hoặc "no".
"""
grade_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        (
            "human",
            "Tài liệu được truy xuất:\n\n{document}\n\nCâu hỏi của người dùng:\n{question}",
        ),
    ]
)

# llm = get_llm(LLM.Local.OLLAMA,"deepseek-r1") => Lỗi do Local Model không nên dùng để Grade with structured
# structured_llm_grader = llm.with_structured_output(GradeDocuments)

llm = get_llm(LLM.Cloud.GOOGLE_CHAT,"gemini-2.5-flash") # Sẽ dùng trong trường hợp đủ token
structured_llm_grader = llm.with_structured_output(GradeDocuments)
retrieval_grader = grade_prompt | structured_llm_grader

def is_document_relevant(question: str, document: str) -> bool:
    result: GradeDocuments = retrieval_grader.invoke(
        {
            "question": question,
            "document": document,
        }
    )
    return result.relevant == "yes"
