from fastapi import FastAPI,HTTPException,UploadFile,File
from pydantic import BaseModel,Field
import traceback,os,shutil
from scripts import rag_ingestion
from scripts.rag_hybrid_search import hybrid_search_with_rrf,create_bm25_index
from scripts.rag_generation import generate_answer
from scripts.rag_ingestion import ingest_document,collection,get_all_child_docs,get_parent_store
from scripts.Rerank_CrossEncoder import rerank

app = FastAPI()

class QuestionRequest(BaseModel):
   query : str

@app.get("/health")
async def get_health():
  return {"message": "Enterprise Multi-Tenant RAG Gateway is live!"}

@app.post("/api/v1/document_ingest")
async def ingest_file(file : UploadFile = File(...)):
  global bm25
  try:
      os.makedirs("./uploads",exist_ok=True)
      
      save_path = f"./uploads/{file.filename}"
      with open(save_path,"wb") as f:
        shutil.copyfileobj(file.file,f)
      
      ingest_document(save_path)
      bm25 = create_bm25_index(rag_ingestion.all_child_docs)
      
      return ({
        "message" : f"Successfully ingested {file.filename}",
        "total_chunks" : rag_ingestion.collection.count()
      })
      
  except Exception as e:
    traceback.print_exc()
    raise HTTPException(status_code=500,detail=str(e))
    
@app.post("/api/v1/query")
async def ask_query(request : QuestionRequest):
  try:
    query = request.query 
    
    # Hybrid retrieval: BM25 + semantic search + RRF
    candidates = hybrid_search_with_rrf(query, collection, bm25,get_all_child_docs(), top_k=10)
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
# in main.py, temporarily
from scripts.rag_ingestion import parent_store

@app.get("/debug/parent-store")
async def debug_parent_store():
    keys = list(parent_store.keys())
    return {
        "total_parents": len(parent_store),
        "sample_keys": keys[:10],
        "content_at_first_key": parent_store[keys[0]] if keys else None
    }