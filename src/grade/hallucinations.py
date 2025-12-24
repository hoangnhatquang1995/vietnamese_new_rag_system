from rag.llm import *
from pydantic import BaseModel,Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from typing import Literal,List 

from rag.documents import format_docs
class GradeHallucinations(BaseModel):
    """Binary score for hallucination present in 'generation' answer."""

    binary_score: str = Field(
        ...,
        description="Answer is grounded in the facts, 'yes' or 'no'"
    )


# llm = get_llm(LLM.Local.OLLAMA,"deepseek-r1") => Lỗi do Local Model không nên dùng để Grade with structured
# structured_llm_grader = llm.with_structured_output(GradeHallucinations)

llm = get_llm(LLM.Cloud.OPEN_AI,"gpt-4o-mini") # Sẽ dùng trong trường hợp đủ token
structured_llm_grader = llm.with_structured_output(GradeHallucinations)

# Prompt
system = """You are a grader assessing whether an LLM generation is grounded in / supported by a set of retrieved facts. \n 
    Give a binary score 'yes' or 'no'. 'Yes' means that the answer is grounded in / supported by the set of facts."""
hallucination_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "Set of facts: \n\n <facts>{documents}</facts> \n\n LLM generation: <generation>{generation}</generation>"),
    ]
)

hallucination_grader = hallucination_prompt | structured_llm_grader


def is_answer_halucinating(question: str, documents: List[Document], generation) -> bool:
    response = hallucination_grader.invoke(
        {"documents": format_docs(documents), "generation": generation}
    )
    return response == "yes"