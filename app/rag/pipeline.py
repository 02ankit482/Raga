from app.rag.loaders import load_pdf_text, extract_images_and_tables
from app.rag.retriever import build_vectorstore, retrieve
from app.rag.generator import generate_answer
from app.rag.constants import TOP_K
from app.logger import setup_logger

rag_logger = setup_logger("rag", "logs/rag.log")


def run_rag(pdf_path: str, query: str) -> dict:
    rag_logger.info("RAG started")
    rag_logger.info(f"PDF path: {pdf_path}")
    # 1. Load data
    texts = load_pdf_text(pdf_path)
    rag_logger.info(f"Loaded {len(texts)} text chunks")
    images, tables = extract_images_and_tables(pdf_path)

    # 2. Build vectorstore
    vectorstore = build_vectorstore(texts)
    rag_logger.info("Vector store built successfully")
    # 3. Retrieve relevant chunks
    results = retrieve(query, vectorstore, top_k=TOP_K)
    rag_logger.info(f"Retrieved {len(results)} relevant chunks")
    # 4. Build context
    context = ""
    log = ""

    for idx, (chunk, score) in enumerate(results, start=1):
        context += chunk + "\n\n"
        log += f"Chunk {idx} | Score: {score:.4f}\n"
        log += chunk[:200] + "\n\n"

    context += f"\nImages found: {len(images)}"
    context += f"\nTables found: {len(tables)}"

    # 5. Generate answer
    rag_logger.info("Calling LLM for generation")

    answer = generate_answer(context, query)
    rag_logger.info("LLM response generated successfully")


    return {
        "result": answer,
        "num_chunks": len(texts),
        "num_images": len(images),
        "num_tables": len(tables),
        "log": log,
    }
