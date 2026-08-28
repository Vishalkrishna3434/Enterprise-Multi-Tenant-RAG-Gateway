from fastapi import FastAPI
from app.routers import query
from app.routers import ingest

app = FastAPI()
app.state.bm25_index = None 

app.include_router(query.router)
app.include_router(ingest.router)

@app.get("/health")
async def get_health():
  return {"message": "Enterprise Multi-Tenant RAG Gateway is live!"}