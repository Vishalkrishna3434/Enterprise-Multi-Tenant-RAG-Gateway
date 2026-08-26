import chromadb
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from scripts.file_loader import load_document

client = chromadb.PersistentClient(path="./chroma_db")

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

collection = client.get_or_create_collection(name="enterprise_rag_children")

all_child_docs = []
parent_store = {} 

def get_all_child_docs():
    return all_child_docs

def get_parent_store():
    return parent_store

def ingest_document(file_path:str):
  raw_text = load_document(file_path)
  # temporarily, inside ingest_document(), right after raw_text = load_document(file_path)
  print(f"Extracted {len(raw_text)} characters from {file_path}")
  # 1. Parent-child Chunking
  parent_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)

  child_splitter = RecursiveCharacterTextSplitter(chunk_size=300,chunk_overlap=50)

  parent_docs = parent_splitter.create_documents([raw_text])

  new_child_docs = []
  
  for local_id,parent_doc in enumerate(parent_docs):
      global_parent_id = f"{file_path}_{local_id}"
      parent_store[global_parent_id] = parent_doc.page_content
      child_docs = child_splitter.create_documents([parent_doc.page_content])
      
      for child in child_docs:
        child.metadata = {"parent_id":global_parent_id,"document":file_path}
        new_child_docs.append(child)
        
  all_child_docs.extend(new_child_docs)
  
  # 2. Generate embeddings

  start_idx = len(all_child_docs)-len(new_child_docs)
  texts = [child.page_content for child in new_child_docs]
  child_embeddings = model.encode(texts).tolist()
  #Alternate way
  """
  all_embeddings = []

  for child in all_child_docs:
      embeddings_child = model.encode(child.page_content)
      all_embeddings.append(embeddings_child)
      
  """

  # 3. Store into Chromadb 

  
  ids = [f"child_{start_idx+i}" for i in range(len(new_child_docs))]
  documents = texts
  metadatas = [child.metadata for child in new_child_docs]

  collection.add(
    embeddings=child_embeddings,
    documents=documents,
    ids=ids,
    metadatas=metadatas
  )
  
  print(f"Successfully stored {len(new_child_docs)} new chunks. Total: {collection.count()}")

