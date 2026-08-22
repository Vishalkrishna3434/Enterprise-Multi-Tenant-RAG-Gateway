from rank_bm25 import BM25Okapi

corpus = [
    "Hello there good man!",
    "It is quite windy in London",
    "How is the weather today?"
]

tokenized_corpus = [doc.lower().split(" ") for doc in corpus]

bm25 = BM25Okapi(tokenized_corpus)

query = "Hello windy today"
tokenized_query = query.lower().split(" ")

scores = bm25.get_scores(tokenized_query)
print("BM25 Scores:",scores)