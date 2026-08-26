import os 
from fastapi import HTTPException

MAX_FILE_SIZE_MB = 20
ALLOWED_EXTENSIONS = {".pdf",".docx",".txt"}

def validate_file_type(filename:str) -> None:
   ext = os.path.splitext(filename)[1].lower()
   
   if ext not in ALLOWED_EXTENSIONS:
     raise HTTPException(status_code=400,
                         detail=f"Unsupported file type '{ext}'.Allowed types: {','.join(ALLOWED_EXTENSIONS)}"
                        )

def validate_file_size(contents : bytes)->None:
   size_mb = len(contents) / (1024 * 1024)
   if size_mb > MAX_FILE_SIZE_MB:
     raise HTTPException(status_code=413,
                         detail=f"File too large ({size_mb:.1f}MB). Max allowed: {MAX_FILE_SIZE_MB}MB"
                        )
   