from rank_bm25 import BM25Okapi
from collections import defaultdict
from app.services.rag_ingestion import model,all_child_docs

bm25 = None

def set_bm25_index(index):
    global bm25
    bm25 = index

def get_bm25_index():
    return bm25

def create_bm25_index(all_child_docs):
  tokenized_corpus = [doc.page_content.lower().split(" ") for doc in all_child_docs]
  
  if not tokenized_corpus:
    return None
  
  return BM25Okapi(tokenized_corpus)

def hybrid_search_with_rrf(query,collection,bm25_engine,all_child_docs,top_k=10,k_constant=60):
    print("Number of child docs:", len(all_child_docs))
    print("BM25 engine:", bm25_engine)
    if bm25_engine is None or not all_child_docs: 
       return []
    
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

    
    
    