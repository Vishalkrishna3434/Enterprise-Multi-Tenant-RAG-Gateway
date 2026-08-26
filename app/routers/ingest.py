
from fastapi import APIRouter,HTTPException,UploadFile,File
import traceback,os,shutil
from app.services.rag_hybrid_search import set_bm25_index,create_bm25_index
from app.services.rag_ingestion import ingest_document,collection,get_all_child_docs

router = APIRouter()

@router.post("/api/v1/document_ingest")
async def ingest_file(file : UploadFile = File(...)):
  try:
      os.makedirs("./uploads",exist_ok=True)
      
      save_path = f"./uploads/{file.filename}"
      with open(save_path,"wb") as f:
        shutil.copyfileobj(file.file,f)
      
      ingest_document(save_path)
      new_bm25 = create_bm25_index(get_all_child_docs())
      set_bm25_index(new_bm25)
      
      return ({
        "message" : f"Successfully ingested {file.filename}",
        "total_chunks" : collection.count()
      })
      
  except Exception as e:
    traceback.print_exc()
    raise HTTPException(status_code=500,detail=str(e))
