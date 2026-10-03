from rank_bm25 import BM25Okapi

from src.retrieval import load_vectorstore
from langchain_core.documents import Document


class HybridRetriever:

    def __init__(self):

        self.vectorstore = load_vectorstore()

        data = self.vectorstore.get(
            include=[
                "documents",
                "metadatas"
            ]
        )

        documents = data["documents"]
        metadatas = data["metadatas"]

        self.documents = []

        for content, metadata in zip(
            documents,
            metadatas
        ):

            document = Document(
                page_content=content,
                metadata=metadata
            )

            self.documents.append(
                document
            )

        tokenized_documents = [
            document.page_content.lower().split()
            for document in self.documents
        ]

        self.bm25 = BM25Okapi(
            tokenized_documents
        )


    def vector_search(
        self,
        query,
        k=5
    ):

        return self.vectorstore.similarity_search(
            query,
            k=k
        )


    def keyword_search(
        self,
        query,
        k=5
    ):

        tokenized_query = query.lower().split()

        scores = self.bm25.get_scores(
            tokenized_query
        )

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda index: scores[index],
            reverse=True
        )

        return [
            self.documents[index]
            for index in ranked_indices[:k]
        ]


    def hybrid_search(
        self,
        query,
        k=5,
        vector_weight=0.5,
        keyword_weight=0.5
    ):

        vector_results = self.vector_search(
            query,
            k=k
        )

        keyword_results = self.keyword_search(
            query,
            k=k
        )

        combined_documents = {}


        # Vector results
        for rank, document in enumerate(
            vector_results
        ):

            key = (
                document.metadata.get("source"),
                document.page_content
            )

            score = (
                (k - rank)
                * vector_weight
            )

            combined_documents[key] = {
                "document": document,
                "score": score
            }


        # Keyword results
        for rank, document in enumerate(
            keyword_results
        ):

            key = (
                document.metadata.get("source"),
                document.page_content
            )

            score = (
                (k - rank)
                * keyword_weight
            )

            if key in combined_documents:

                combined_documents[key]["score"] += score

            else:

                combined_documents[key] = {
                    "document": document,
                    "score": score
                }


        ranked_results = sorted(
            combined_documents.values(),
            key=lambda item: item["score"],
            reverse=True
        )


        return [
            item["document"]
            for item in ranked_results[:k]
        ]