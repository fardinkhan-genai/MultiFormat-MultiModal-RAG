from src.hybrid_retrieval import HybridRetriever
from src.reranker import Reranker

from src.retrieval import (
    format_context,
    extract_sources
)

from src.generator import generate_answer


def ask_rag(
    query,
    candidate_k=10,
    final_k=5
):

    print("\n====================================")
    print("RAG PIPELINE")
    print("====================================")


    # 1. Hybrid retrieval

    retriever = HybridRetriever()

    candidates = retriever.hybrid_search(
        query=query,
        k=candidate_k
    )


    print(
        f"Candidates retrieved: "
        f"{len(candidates)}"
    )


    # 2. Reranking

    reranker = Reranker()

    results = reranker.rerank(
        query=query,
        documents=candidates,
        top_k=final_k
    )


    print(
        f"Documents after reranking: "
        f"{len(results)}"
    )


    # 3. Build context

    context = format_context(
        results
    )


    # 4. Generate answer

    answer = generate_answer(
        query=query,
        context=context
    )


    # 5. Extract sources

    sources = extract_sources(
        results
    )


    return answer, sources, results