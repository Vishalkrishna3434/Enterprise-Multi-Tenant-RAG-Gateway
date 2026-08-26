import os 

def load_document (file_path:str)->str:
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext==".txt":
      with open(file_path,"r",encoding="utf-8") as f:
       return f.read()
    
    elif ext==".pdf":
      from pypdf import PdfReader
      reader = PdfReader(file_path)
      return "\n".join(page.extract_text() for page in reader.pages)
    
    elif ext==".docx":
      from docx import Document as DocxDocument
      doc = DocxDocument(file_path)
      return "\n".join(para.text for para in doc.paragraphs)
    
    else :
      raise ValueError(f"Unsupported file type: {ext}")