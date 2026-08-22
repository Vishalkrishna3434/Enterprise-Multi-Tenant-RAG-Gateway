from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field
import traceback
from scripts.rag_ingestion import collection, all_child_docs,model
from scripts.rag_hybrid_search import hybrid_search_with_rrf,bm25

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

    print(f"Top Hybrid Search Result for query: '{query}'")
    print("-" * 50)
    
    response_results = []
    for idx,res in enumerate(results):
        print(f"Result {idx+1} Parent ID:{res.metadata['parent_id']}")
        print(res.page_content)
        print("-"*50)
        
        response_results.append({
          "parent_id" : res.metadata["parent_id"],
          "page_content":res.page_content
        })
    
    return {
      "query": query,
      "results" : response_results
    }

  except Exception as e:
    traceback.print_exec()
    raise HTTPException(status_code=500,detail=str(e))