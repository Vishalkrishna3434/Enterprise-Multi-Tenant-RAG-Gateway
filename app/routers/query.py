from fastapi import APIRouter,HTTPException
from app.services.rag_hybrid_search import hybrid_search_with_rrf,get_bm25_index
from app.services.rag_generation import generate_answer
from app.services.rag_reranker import rerank
from app.schemas.requests import QuestionRequest
from app.services.rag_ingestion import collection,get_all_child_docs,get_parent_store
import traceback

router = APIRouter()
    
@router.post("/api/v1/query")
async def ask_query(request : QuestionRequest):
  try:
    query = request.query 
    
    bm25_index = get_bm25_index
    if bm25_index is None:
        raise HTTPException(
            status_code=400,
            detail="No documents have been ingested yet. Upload a document via /api/v1/document_ingest first."
        )
    
    # Hybrid retrieval: BM25 + semantic search + RRF
    candidates = hybrid_search_with_rrf(query, collection, get_bm25_index(),get_all_child_docs(), top_k=10)
    results = rerank(query,candidates,top_k=2)
    
    response_results = []
    parent_ids_seen = set()
    parent_contexts = []
    for idx,res in enumerate(results):
        pid = res.metadata["parent_id"]
        response_results.append({
          "parent_id" : pid,
          "page_content": res.page_content 
        })
        if pid not in parent_ids_seen:
          parent_contexts.append(get_parent_store()[pid])
          parent_ids_seen.add(pid)
    
    # Generate answer using parent contexts
    answer = await generate_answer(query,parent_contexts)
    
    return {
      "query": query,
      "results" : response_results,
      "answer" : answer 
    }

  except Exception as e:
    traceback.print_exc()
    raise HTTPException(status_code=500,detail=str(e))
