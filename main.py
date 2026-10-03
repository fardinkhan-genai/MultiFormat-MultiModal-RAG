from src.ingestion.universal_ingestion import build_knowledge_base


print("====================================")
print("MultiFormat Multimodal RAG")
print("====================================")


DATA_DIRECTORY = "data"


vectorstore = build_knowledge_base(DATA_DIRECTORY)


print("\n====================================")
print("Step 11 completed successfully!")
print("====================================")