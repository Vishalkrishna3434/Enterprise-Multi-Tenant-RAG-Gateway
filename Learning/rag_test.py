import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

sentences =[
  "The sky is awesome",
  "The light is there"
]


embeddings = model.encode(sentences)

print(embeddings.shape)

chroma_client = chromadb.Client()

collection = chroma_client.get_or_create_collection(name="my_collection")

collection.upsert(
  documents=[
    "How are you doing?",
    "are you good?"
  ],ids=["id1","id2"]
)

results = collection.query(
  query_texts = ["This is a document about florida"],
  n_results=2
)

print(results)

