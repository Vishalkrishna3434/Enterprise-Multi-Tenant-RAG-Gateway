import chromadb
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from scripts.file_loader import load_document

client = chromadb.PersistentClient(path="./chroma_db")

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

collection = client.get_or_create_collection(name="enterprise_rag_children")

all_child_docs = []
parent_store = {} 

def ingest_document(file_path:str):
  raw_text = load_document(file_path)
 
  # 1. Parent-child Chunking
  parent_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)

  child_splitter = RecursiveCharacterTextSplitter(chunk_size=300,chunk_overlap=50)

  parent_docs = parent_splitter.create_documents([raw_text])


  for parent_id,parent_doc in enumerate(parent_docs):
      parent_store[parent_id] = parent_doc.page_content
      child_docs = child_splitter.create_documents([parent_doc.page_content])
      
      for child in child_docs:
        child.metadata = {"parent_id":parent_id,"document":file_path}
        all_child_docs.append(child)

  # 2. Generate embeddings


  texts = [child.page_content for child in all_child_docs]
  child_embeddings = model.encode(texts).tolist()
  #Alternate way
  """
  all_embeddings = []

  for child in all_child_docs:
      embeddings_child = model.encode(child.page_content)
      all_embeddings.append(embeddings_child)
      
  """

  # 3. Store into Chromadb 


  ids = [f"child_{i}" for i in range(len(all_child_docs))]
  documents = [child.page_content for child in all_child_docs]
  metadatas = [child.metadata for child in all_child_docs]

  collection.add(
    embeddings=child_embeddings,
    documents=documents,
    ids=ids,
    metadatas=metadatas
  )

  print(f"Successfully Stored {collection.count()} child chunks in ChromaDB")

