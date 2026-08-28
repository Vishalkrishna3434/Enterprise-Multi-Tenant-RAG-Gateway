from app.services.rag_ingestion import model

def vector_search(query: str, collection, top_k: int) -> list[int]:
    """Returns child_doc indices ranked by semantic similarity, best first."""
    query_embedding = model.encode(query).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    ids = results['ids'][0]
    return [int(doc_id.split("_")[1]) for doc_id in ids]