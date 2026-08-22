from rank_bm25 import BM25Okapi
from ..scripts.rag_ingestion import collection, all_child_docs,model
from ..scripts.rag_hybrid_search import hybrid_search_with_rrf

tokenized_corpus = [doc.page_content.lower().split(" ") for doc in all_child_docs]
bm25 = BM25Okapi(tokenized_corpus)

query_text = "What is the multi-tenant architecture?"
results = hybrid_search_with_rrf(query_text, collection, bm25, all_child_docs, top_k=2)

print(f"Top Hybrid Search Result for query: '{query_text}'")
print("-" * 50)
for idx,res in enumerate(results):
    print(f"Result {idx+1} Parent ID:{res.metadata['parent_id']}")
    print(res.page_content)
    print("-"*50)