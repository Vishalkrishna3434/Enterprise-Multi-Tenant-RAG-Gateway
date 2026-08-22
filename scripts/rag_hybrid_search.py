from collections import defaultdict
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def hybrid_search_with_rrf(query,collection,bm25_engine,all_child_docs,top_k=3,k_constant=60):
    
    tokenized_query = query.lower().split(" ")
    bm25_scores = bm25_engine.get_scores(tokenized_query)
    
    bm25_ranked_indices = sorted(range(len(bm25_scores)),key=lambda i: bm25_scores[i],reverse=True)
    
    query_embedding = model.encode(query).tolist()
    
    vector_results = collection.query(
      query_embeddings=[query_embedding],
      n_results=len(all_child_docs)
    )
    
    vector_ids = vector_results['ids'][0]
    vector_ranked_ids = [int(vid.split("_")[1]) for vid in vector_ids]
    
    rrf_scores = defaultdict(float)
    
    for rank,doc_idx in enumerate(bm25_ranked_indices):
       rrf_scores[doc_idx] += 1.0 / (k_constant + rank + 1) 
    
    
    for rank,doc_idx in enumerate(vector_ranked_ids):
        rrf_scores[doc_idx] += 1.0 / (k_constant + rank + 1)
        
    final_sorted_indices = sorted(rrf_scores.keys(),key = lambda idx: rrf_scores[idx],reverse=True)
    
    top_indices = final_sorted_indices[:top_k]
    return [all_child_docs[i] for i in top_indices]
  
query_text = "What is the multi-tenant architecture?"
results = hybrid_search_with_rrf(query_text, collection, bm25, all_child_docs, top_k=2)

print(f"Top Hybrid Search Result for query: '{query_text}'")
print("-" * 50)
for idx,res in enumerate(results):
    print(f"Result {idx+1} Parent ID:{res.metadata['parent_id']}")
    print(res.page_content)
    print("-"*50)
    
    
    