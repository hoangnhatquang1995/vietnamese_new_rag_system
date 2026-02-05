from __future__ import annotations

from typing import Any, Dict, List, Optional, TypedDict

from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.documents import Document
from langgraph.graph import END, StateGraph
from sqlalchemy import text

import rag
from data.sqldb import engine
from rag.chatbot import prompt as rag_prompt


class AgentState(TypedDict, total=False):
    question: str
    query: str
    retrieved_docs: List[Document]
    sql_result: Optional[List[Dict[str, Any]]]
    answer: str
    iterations: int
    trace: List[Dict[str, Any]]


NOT_FOUND_TEXT = "Không tìm thấy thông tin này trong các bài viết được cung cấp."


def _append_trace(state: AgentState, event: Dict[str, Any]) -> None:
    trace = state.get("trace") or []
    trace.append(event)
    state["trace"] = trace


def _select_only_sql(sql: str, *, limit: int = 50) -> str:
    statement = (sql or "").strip()
    if not statement:
        return ""

    lowered = statement.lower().lstrip()
    if not lowered.startswith("select"):
        raise ValueError("Only SELECT queries are allowed")

    # Disallow multiple statements.
    if ";" in statement.rstrip(";"):
        raise ValueError("Multiple statements are not allowed")

    # Apply a row limit if user didn't.
    if " limit " not in lowered:
        statement = f"{statement} LIMIT {int(limit)}"

    return statement


def _run_select(sql: str) -> List[Dict[str, Any]]:
    """Run a read-only SELECT using the shared SQLAlchemy engine."""

    if not sql:
        return []

    with engine.connect() as conn:
        result = conn.execute(text(sql))
        # Use mappings() to get dict-like rows.
        return [dict(row) for row in result.mappings().all()]


def _route(state: AgentState) -> str:
    question = (state.get("question") or "").strip()
    state["query"] = state.get("query") or question

    # Simple routing: explicit SQL prefix.
    if question.lower().startswith("sql:"):
        state["query"] = question[4:].strip()
        _append_trace(state, {"type": "route", "next": "sql_query"})
        return "sql_query"

    _append_trace(state, {"type": "route", "next": "rag_retrieve"})
    return "rag_retrieve"


def _sql_query(state: AgentState) -> AgentState:
    raw_query = (state.get("query") or "").strip()
    safe_sql = _select_only_sql(raw_query)
    rows = _run_select(safe_sql)
    state["sql_result"] = rows
    _append_trace(state, {"type": "sql", "sql": safe_sql, "rows": len(rows)})
    return state


def _rag_retrieve(state: AgentState) -> AgentState:
    query = (state.get("query") or "").strip() or (state.get("question") or "").strip()
    docs = rag.db.search(query)
    state["retrieved_docs"] = docs

    _append_trace(
        state,
        {
            "type": "rag_retrieve",
            "query": query,
            "k": 10,
            "docs": [
                {
                    "source": d.metadata.get("source"),
                    "title": d.metadata.get("title"),
                    "published_time": d.metadata.get("published_time"),
                    "news": d.metadata.get("news"),
                }
                for d in docs
            ],
        },
    )
    return state


def _rewrite_query(state: AgentState) -> AgentState:
    """Rewrite query once if retrieval seems insufficient."""

    question = state.get("question") or ""
    prev_query = state.get("query") or question

    prompt = (
        "Bạn là chuyên gia tối ưu truy vấn tìm kiếm cho hệ thống RAG tin tức tiếng Việt.\n"
        "Hãy viết lại *một* câu truy vấn ngắn gọn để truy xuất tin tức phù hợp nhất.\n"
        "- Chỉ trả về đúng 1 dòng truy vấn (không giải thích).\n\n"
        f"Câu hỏi: {question}\n"
        f"Truy vấn hiện tại: {prev_query}\n"
    )

    msg = rag.llm.invoke(prompt)
    new_query = getattr(msg, "content", None) or str(msg)
    new_query = new_query.strip().strip('"')

    if new_query:
        state["query"] = new_query

    _append_trace(state, {"type": "rewrite_query", "from": prev_query, "to": state.get("query")})
    return state


def _answer(state: AgentState) -> AgentState:
    docs = list(state.get("retrieved_docs") or [])

    sql_result = state.get("sql_result")
    if sql_result is not None:
        sql_text = "KẾT QUẢ TRUY VẤN SQLITE (read-only):\n" + str(sql_result)
        docs.append(Document(page_content=sql_text, metadata={"source": "sqlite", "title": "SQL result"}))

    question_answer_chain = create_stuff_documents_chain(rag.llm, rag_prompt)
    res = question_answer_chain.invoke({"context": docs, "input": state.get("question")})

    if isinstance(res, str):
        answer = res
    elif isinstance(res, dict):
        answer = res.get("answer") or res.get("output_text") or str(res)
    else:
        answer = getattr(res, "content", None) or str(res)

    answer = (answer or "").strip()
    state["answer"] = answer
    _append_trace(state, {"type": "answer", "chars": len(answer)})

    state["iterations"] = int(state.get("iterations") or 0) + 1
    return state


def _should_retry(state: AgentState) -> str:
    answer = (state.get("answer") or "").strip()
    iterations = int(state.get("iterations") or 0)

    if iterations < 2 and (NOT_FOUND_TEXT in answer or len(state.get("retrieved_docs") or []) == 0):
        _append_trace(state, {"type": "route", "next": "rewrite_query"})
        return "rewrite_query"

    _append_trace(state, {"type": "route", "next": "end"})
    return "end"


def _build_agent():
    graph = StateGraph(AgentState)

    graph.add_node("route", _route)
    graph.add_node("sql_query", _sql_query)
    graph.add_node("rag_retrieve", _rag_retrieve)
    graph.add_node("rewrite_query", _rewrite_query)
    graph.add_node("answer", _answer)

    graph.set_entry_point("route")
    graph.add_conditional_edges(
        "route",
        _route,
        {
            "sql_query": "sql_query",
            "rag_retrieve": "rag_retrieve",
        },
    )

    graph.add_edge("sql_query", "answer")
    graph.add_edge("rag_retrieve", "answer")

    graph.add_conditional_edges(
        "answer",
        _should_retry,
        {
            "rewrite_query": "rewrite_query",
            "end": END,
        },
    )
    graph.add_edge("rewrite_query", "rag_retrieve")

    return graph.compile()


_AGENT = _build_agent()


def run_agent(question: str, *, include_trace: bool = False) -> Dict[str, Any]:

    state: AgentState = {
        "question": question,
        "query": question,
        "iterations": 0,
        "trace": [],
    }

    final_state = _AGENT.invoke(state)
    docs = final_state.get("retrieved_docs") or []

    sources = [
        {
            "source": d.metadata.get("source"),
            "title": d.metadata.get("title"),
            "published_time": d.metadata.get("published_time"),
            "news": d.metadata.get("news"),
        }
        for d in docs
    ]

    result: Dict[str, Any] = {
        "answer": final_state.get("answer") or "",
        "sources": sources,
    }

    if include_trace:
        result["trace"] = final_state.get("trace") or []

    return result
