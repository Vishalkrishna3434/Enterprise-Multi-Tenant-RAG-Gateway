from app.services.rag_vector_search import vector_search
from app.services.rag_bm25_search import bm25_search
from app.services.rag_fusion import reciprocal_rank_fusion

def hybrid_search_with_rrf(query, collection, bm25_engine, all_child_docs, top_k=10, k_constant=60):
    """Vector + BM25, fused via RRF."""
    if bm25_engine is None or not all_child_docs:
        return []

    bm25_ranked = bm25_search(query, bm25_engine, top_k=len(all_child_docs))
    vector_ranked = vector_search(query, collection, top_k=len(all_child_docs))
    fused = reciprocal_rank_fusion([bm25_ranked, vector_ranked], k_constant)

    valid_docs = [all_child_docs[i] for i in fused if 0 <= i < len(all_child_docs)]
    return valid_docs[:top_k]