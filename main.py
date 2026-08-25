from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field
import traceback
from scripts.rag_ingestion import collection, all_child_docs,model,parent_store
from scripts.rag_hybrid_search import hybrid_search_with_rrf,bm25
from scripts.rag_generation import generate_answer

app = FastAPI()

class QuestionRequest(BaseModel):
   query : str

@app.get("/health")
async def get_health():
  return {"message": "Enterprise Multi-Tenant RAG Gateway is live!"}

@app.post("/api/v1/query")
async def ask_query(request : QuestionRequest):
  try:
    query = request.query 
    
    results = hybrid_search_with_rrf(query, collection, bm25, all_child_docs, top_k=2)

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
          parent_contexts.append(parent_store[pid])
          parent_ids_seen.add(pid)
          
    answer = await generate_answer(query,parent_contexts)
    
    return {
      "query": query,
      "results" : response_results,
      "answer" : answer 
    }

  except Exception as e:
    traceback.print_exc()
    raise HTTPException(status_code=500,detail=str(e))