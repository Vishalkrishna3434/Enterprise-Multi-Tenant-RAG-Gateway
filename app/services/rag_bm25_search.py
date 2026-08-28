from rank_bm25 import BM25Okapi

def create_bm25_index(all_child_docs):
    tokenized_corpus = [doc.page_content.lower().split(" ") for doc in all_child_docs]
    if not tokenized_corpus:
        return None
    return BM25Okapi(tokenized_corpus)

def bm25_search(query: str, bm25_engine, top_k: int) -> list[int]:
    """Returns child_doc indices ranked by lexical match, best first."""
    tokenized_query = query.lower().split(" ")
    scores = bm25_engine.get_scores(tokenized_query)
    ranked_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
    return ranked_indices[:top_k]