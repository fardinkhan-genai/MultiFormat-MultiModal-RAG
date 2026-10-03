from sentence_transformers import CrossEncoder


RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"


class Reranker:

    def __init__(self):

        print("Loading reranker...")

        self.model = CrossEncoder(
            RERANKER_MODEL
        )

        print("Reranker loaded.")


    def rerank(
        self,
        query,
        documents,
        top_k=5
    ):

        if not documents:
            return []

        pairs = [
            [
                query,
                document.page_content
            ]
            for document in documents
        ]

        scores = self.model.predict(
            pairs
        )

        ranked_documents = sorted(
            zip(documents, scores),
            key=lambda item: item[1],
            reverse=True
        )

        return [
            document
            for document, score
            in ranked_documents[:top_k]
        ]