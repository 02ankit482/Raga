from typing import List, Tuple

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


from app.rag.constants import (
    EMBEDDING_MODEL_NAME,
    TOP_K,
)

_embedding_fn = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)



def build_vectorstore(texts: List[str]) -> FAISS:
    if not texts:
        raise ValueError("No texts provided to build vectorstore")

    return FAISS.from_texts(texts, _embedding_fn)


def retrieve(
    query: str,
    vectorstore: FAISS,
    top_k: int = TOP_K,
) -> List[Tuple[str, float]]:
    if not query:
        raise ValueError("Query cannot be empty")

    results = vectorstore.similarity_search_with_score(
        query, k=top_k
    )

    return [(doc.page_content, float(score)) for doc, score in results]
