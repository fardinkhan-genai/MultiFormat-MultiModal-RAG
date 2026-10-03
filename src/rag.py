from src.hybrid_retrieval import HybridRetriever
from src.reranker import Reranker

from src.retrieval import (
    format_context,
    extract_sources
)

from src.generator import generate_answer


class UniversalRAG:

    def __init__(
        self,
        candidate_k=10,
        final_k=5
    ):

        self.candidate_k = candidate_k
        self.final_k = final_k

        print("Initializing Universal RAG...")

        self.retriever = HybridRetriever()

        self.reranker = Reranker()

        print("Universal RAG ready.")


    def ask(self, query):

        print("\n====================================")
        print("UNIVERSAL RAG")
        print("====================================")

        print(f"Question: {query}")


        # 1. Hybrid Retrieval

        candidates = self.retriever.hybrid_search(
            query=query,
            k=self.candidate_k
        )

        print(
            f"Retrieved candidates: "
            f"{len(candidates)}"
        )


        # 2. Reranking

        results = self.reranker.rerank(
            query=query,
            documents=candidates,
            top_k=self.final_k
        )

        print(
            f"Final documents: "
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


        return {
            "answer": answer,
            "sources": sources,
            "documents": results
        }