from src.query_router import classify_query
from src.hybrid_retrieval import HybridRetriever
from src.retrieval import format_context
from src.generator import generate_answer


def run_query(query):

    print("\n====================================")
    print("QUERY ENGINE")
    print("====================================")

    # Step 1 — Classify query

    route = classify_query(query)

    print("Query:")
    print(query)

    print("\nDetected route:")
    print(route)


    # Step 2 — TEXT route

    if route == "TEXT":

        retriever = HybridRetriever()

        results = retriever.hybrid_search(
            query=query,
            k=5
        )

        context = format_context(
            results
        )

        answer = generate_answer(
            query=query,
            context=context
        )

        return answer, results


    # Step 3 — TABLE route

    elif route == "TABLE":

        return (
            "TABLE processing will be implemented "
            "in the next stage.",
            []
        )


    # Step 4 — VISION route

    elif route == "VISION":

        return (
            "VISION processing will be implemented "
            "in the next stage.",
            []
        )


    # Step 5 — AUDIO route

    elif route == "AUDIO":

        return (
            "AUDIO processing will be implemented "
            "in the next stage.",
            []
        )


    # Step 6 — VIDEO route

    elif route == "VIDEO":

        return (
            "VIDEO processing will be implemented "
            "in the next stage.",
            []
        )