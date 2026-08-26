from sentence_transformers import CrossEncoder

cross_encoder = CrossEncoder("cross-encoder/stsb-distilroberta-base")

def rerank(query:str,candidates:list,top_k:int=2):
  if not candidates:
     return []
  
  pairs = [[query,doc.page_content] for doc in candidates]
  scores = cross_encoder.predict(pairs)
  
  for doc,score in zip(candidates,scores):
      print(f"{score:.3f} | {doc.metadata['parent_id']} | {doc.page_content[:60]}")
  
  ranked = sorted(zip(candidates,scores),key= lambda x: x[1],reverse=True)
  return [doc for doc,score in ranked[:top_k]]
  

  
  