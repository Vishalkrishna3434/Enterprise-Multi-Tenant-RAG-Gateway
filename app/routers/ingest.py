from fastapi import APIRouter,HTTPException,UploadFile,File,Request
import traceback,os,asyncio
from app.services.rag_bm25_search import create_bm25_index
from app.services.rag_ingestion import ingest_document,collection,get_all_child_docs
from app.services.guardrails import validate_file_type,validate_file_size

router = APIRouter()

@router.post("/api/v1/document_ingest")
async def ingest_file(request: Request, file: UploadFile = File(...)):
  try:
      validate_file_type(file.filename) 
      
      contents = await file.read()
      validate_file_size(contents)
      
      os.makedirs("./uploads",exist_ok=True)
      save_path = f"./uploads/{file.filename}"
      with open(save_path,"wb") as f:
        f.write(contents)
      
      await asyncio.to_thread(ingest_document,save_path)
      new_bm25 = await asyncio.to_thread(create_bm25_index,get_all_child_docs())
      request.app.state.bm25_index = new_bm25
      
      return ({
        "message" : f"Successfully ingested {file.filename}",
        "total_chunks" : collection.count()
      })
  
  except HTTPException:
      raise   
  except Exception as e:
    traceback.print_exc()
    raise HTTPException(status_code=500,detail=str(e))
