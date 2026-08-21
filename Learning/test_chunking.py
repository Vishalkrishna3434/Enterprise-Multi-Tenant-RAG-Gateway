from langchain_text_splitters import RecursiveCharacterTextSplitter

sample_file_path = "./sample.txt"

with open(sample_file_path,"r") as f:
      raw_text = f.read()
      
parent_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)

child_splitter = RecursiveCharacterTextSplitter(chunk_size=300,chunk_overlap=50)

parent_docs = parent_splitter.create_documents([raw_text])

all_child_chunks=[]
parent_store={}

for parent_id,parent_doc in enumerate(parent_docs):
    parent_store[parent_id] = parent_doc.page_content
    
    child_docs = child_splitter.create_documents([parent_doc.page_content])
    for child in child_docs:
        child.metadata={"parent_id": parent_id,"document":sample_file_path}
        all_child_chunks.append(child)

sample_child = all_child_chunks[0]
retrieved_parent_id = sample_child.metadata["parent_id"]
resolved_parent_context = parent_store[retrieved_parent_id]

print("Sample Child Chunk Content:")
print(f"'{sample_child.page_content}'")
print(f"Metadata: {sample_child.metadata}")
print("-" * 50)
print("Resolved Parent Context Block:")
print(f"'{resolved_parent_context[:300]}...'")

